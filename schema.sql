drop schema if exists spaceiq cascade;
create schema spaceiq;
create table spaceiq.space_types (
  idx text primary key,
  name text
);
create table spaceiq.spaces (
  idx text primary key,
  space_type text references spaceiq.space_types(idx),
  width int,
  x int,
  y int,
  name text
);
create table spaceiq.departments (
  idx text primary key,
  name text
);
create table spaceiq.regions (
  idx text primary key,
  name text
);
create table spaceiq.employees (
  idx text primary key,
    name text,
    email text,
    region text references spaceiq.regions(idx),
    department text references spaceiq.departments(idx)
);
create table spaceiq.booking_schedules (
  idx serial primary key,
  employee text references spaceiq.employees(idx),
  space text references spaceiq.spaces(idx),
  start_dt timestamp,
  end_dt timestamp,
  schedule_type text,
  unique (employee, space, start_dt, end_dt, schedule_type)
);
create table spaceiq.bookings (
  idx text primary key,
  booking_employee text references spaceiq.employees(idx),
  start_dt timestamp,
  end_dt timestamp,
  passed_health_check boolean,
  checked_in boolean,
  auto_released_at timestamp,
  part_of_schedule int references spaceiq.booking_schedules(idx),
  space text references spaceiq.spaces(idx)
);