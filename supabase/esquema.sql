-- Esquema de la App GYM en Supabase.
--
-- Cómo se usa: en Supabase, SQL Editor → New query → pegar este archivo
-- completo → Run. Se puede correr más de una vez sin romper nada.
--
-- Idea general:
-- - Cada fila tiene dueño (user_id). Nadie ve ni toca filas de otro usuario
--   (Row Level Security). Por eso la clave pública (anon / publishable) puede
--   ir en el celular sin riesgo: sin sesión iniciada no se lee nada.
-- - Los id los crea el celular (uuid), así una serie anotada sin señal ya
--   tiene su id definitivo y se puede subir más tarde sin duplicarse.
-- - Nada se borra de verdad: se marca borrado = true, para que el borrado
--   también llegue a los otros aparatos.
-- - actualizado_en lo pone el celular (cuándo cambió el dato).
--   servidor_en lo pone la base (cuándo llegó). El celular baja "lo que llegó
--   después de mi última bajada" usando servidor_en.
-- - Si llegan dos versiones de la misma fila, gana la de actualizado_en más
--   nuevo (la más reciente según quien la editó).

-- ---------------------------------------------------------------------------
-- Funciones comunes
-- ---------------------------------------------------------------------------

create or replace function public.gym_al_guardar()
returns trigger
language plpgsql
as $$
begin
  -- El dueño siempre es quien está conectado; no se puede escribir a nombre de otro.
  new.user_id := auth.uid();
  if tg_op = 'UPDATE' then
    -- Una versión más vieja que llega tarde no pisa a la más nueva.
    if new.actualizado_en < old.actualizado_en then
      return null;
    end if;
    new.creado_en := old.creado_en;
  end if;
  new.servidor_en := clock_timestamp();
  return new;
end;
$$;

-- ---------------------------------------------------------------------------
-- Rutinas: cada día de entrenamiento que arma el usuario en Editar.
-- Los slots (con sus alternativas A/B/C) van en un solo campo JSON porque
-- siempre se leen y se editan juntos.
-- ---------------------------------------------------------------------------

create table if not exists public.rutinas (
  id             uuid primary key,
  user_id        uuid not null default auth.uid() references auth.users (id) on delete cascade,
  nombre         text not null,
  orden          integer not null default 0,          -- posición en la rotación
  slots          jsonb not null default '[]'::jsonb,
  borrado        boolean not null default false,
  creado_en      timestamptz not null default now(),
  actualizado_en timestamptz not null default now(),
  servidor_en    timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Sesiones: cada vez que se entrena.
-- ---------------------------------------------------------------------------

create table if not exists public.sesiones (
  id             uuid primary key,
  user_id        uuid not null default auth.uid() references auth.users (id) on delete cascade,
  rutina_id      uuid,                                -- puede quedar null si se borra la rutina
  rutina_nombre  text,                                -- copia del nombre, por si la rutina cambia
  inicio         timestamptz not null default now(),
  fin            timestamptz,
  notas          text,
  borrado        boolean not null default false,
  creado_en      timestamptz not null default now(),
  actualizado_en timestamptz not null default now(),
  servidor_en    timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Series: el registro en sí. Una fila por serie hecha.
-- ---------------------------------------------------------------------------

create table if not exists public.series (
  id             uuid primary key,
  user_id        uuid not null default auth.uid() references auth.users (id) on delete cascade,
  sesion_id      uuid not null,
  ejercicio_id   text not null,                       -- id de data/ejercicios.json
  slot_id        text,                                -- slot de la rutina (null si se agregó suelto)
  opcion         text check (opcion in ('A', 'B', 'C')),
  posicion       smallint,                            -- en qué lugar de la sesión se hizo el ejercicio (1º, 2º...)
  numero         smallint not null,                   -- número de serie dentro del ejercicio (1, 2, 3...)
  peso           numeric(6, 2) check (peso >= 0),
  unidad         text not null default 'kg' check (unidad in ('kg', 'lb')),
  reps           smallint check (reps >= 0),
  rir            smallint check (rir between 0 and 10),
  drop_de        uuid,                                -- si es un drop set, la serie de la que sale
  biserie_con    text,                                -- slot con el que va en biserie, si aplica
  aviso_orden    text,                                -- advertencia de orden aceptada, si la hubo
  hecha_en       timestamptz not null default now(),
  borrado        boolean not null default false,
  creado_en      timestamptz not null default now(),
  actualizado_en timestamptz not null default now(),
  servidor_en    timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Ajustes: una fila por usuario (metas semanales por músculo, unidades, etc.).
-- ---------------------------------------------------------------------------

create table if not exists public.ajustes (
  id             uuid primary key,                    -- el celular usa el mismo id que el usuario
  user_id        uuid not null default auth.uid() references auth.users (id) on delete cascade,
  datos          jsonb not null default '{}'::jsonb,
  borrado        boolean not null default false,
  creado_en      timestamptz not null default now(),
  actualizado_en timestamptz not null default now(),
  servidor_en    timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Índices: bajar cambios por usuario y buscar la sesión anterior de un ejercicio.
-- ---------------------------------------------------------------------------

create index if not exists rutinas_cambios  on public.rutinas  (user_id, servidor_en);
create index if not exists sesiones_cambios on public.sesiones (user_id, servidor_en);
create index if not exists series_cambios   on public.series   (user_id, servidor_en);
create index if not exists ajustes_cambios  on public.ajustes  (user_id, servidor_en);
create index if not exists series_ejercicio on public.series   (user_id, ejercicio_id, hecha_en desc);
create index if not exists series_sesion    on public.series   (sesion_id);

-- ---------------------------------------------------------------------------
-- Triggers y permisos (Row Level Security), iguales para las cuatro tablas.
-- ---------------------------------------------------------------------------

do $$
declare
  t text;
begin
  foreach t in array array['rutinas', 'sesiones', 'series', 'ajustes'] loop
    execute format('drop trigger if exists al_guardar on public.%I', t);
    execute format(
      'create trigger al_guardar before insert or update on public.%I
         for each row execute function public.gym_al_guardar()', t);

    execute format('alter table public.%I enable row level security', t);
    execute format('drop policy if exists solo_dueno on public.%I', t);
    execute format(
      'create policy solo_dueno on public.%I for all to authenticated
         using (user_id = (select auth.uid()))
         with check (user_id = (select auth.uid()))', t);

    -- Sin sesión iniciada no hay acceso. Borrar de verdad tampoco: se usa borrado = true.
    execute format('revoke all on public.%I from anon', t);
    execute format('revoke delete, truncate on public.%I from authenticated', t);
    execute format('grant select, insert, update on public.%I to authenticated', t);
  end loop;
end;
$$;
