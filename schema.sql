drop schema if exists spaceiq cascade;
create schema spaceiq;
create table spaceiq.seats (
  idx serial primary key,
  name text
);
create table spaceiq.departments (
  idx serial primary key,
  name text
);
create table spaceiq.regions (
  idx serial primary key,
  name text
);
create table spaceiq.employees (
  idx serial primary key,
    name text,
    email text,
    region int references spaceiq.regions(idx),
    department_id int references spaceiq.departments(idx)
);
create table spaceiq.booking_schedule (
  idx serial primary key,
  employee int references spaceiq.employees(idx),
  seat int references spaceiq.seats(idx),
  start_dt timestamp,
  end_dt timestamp,
  schedule_type text
);
create table spaceiq.booking (
  idx serial primary key,
  booking_employee int references spaceiq.employees(idx),
  start_dt timestamp,
  end_dt timestamp,
  passed_health_check boolean,
  checked_in boolean,
  auto_released_at timestamp,
  part_of_schedule int references spaceiq.booking_schedule(idx),
  seat int references spaceiq.seats(idx)
);