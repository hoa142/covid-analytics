truncate table public.covid_cases_temp;
copy public.covid_cases_temp from 's3://covid-analytics-20/{{ params.file_name }}'
    iam_role '{{ params.redshift_iam_role }}' csv ignoreheader 1;

begin transaction;

delete from public.covid_cases
using public.covid_cases_temp
where public.covid_cases.country = public.covid_cases_temp.country
and public.covid_cases.date = public.covid_cases_temp.date;

insert into public.covid_cases
select * from public.covid_cases_temp;

end transaction;
