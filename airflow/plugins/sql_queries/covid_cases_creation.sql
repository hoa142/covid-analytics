CREATE TABLE IF NOT EXISTS public.covid_cases
(
	id VARCHAR(256) NOT NULL  ENCODE lzo
	,country VARCHAR(256) NOT NULL  ENCODE lzo
	,country_code VARCHAR(256)   ENCODE lzo
	,slug VARCHAR(256)   ENCODE lzo
	,new_confirmed INTEGER   ENCODE az64
	,total_confirmed BIGINT   ENCODE az64
	,new_deaths INTEGER   ENCODE az64
	,total_deaths BIGINT   ENCODE az64
	,new_recovered INTEGER   ENCODE az64
	,total_recovered BIGINT   ENCODE az64
	,"time" TIMESTAMP WITHOUT TIME ZONE   ENCODE RAW
	,date DATE NOT NULL  ENCODE RAW
	,UNIQUE (country, date)
)
DISTSTYLE KEY
 DISTKEY (country)
 SORTKEY (
	date
	)
;

CREATE TABLE IF NOT EXISTS public.covid_cases_temp
(
	id VARCHAR(256) NOT NULL  ENCODE lzo
	,country VARCHAR(256) NOT NULL  ENCODE lzo
	,country_code VARCHAR(256)   ENCODE lzo
	,slug VARCHAR(256)   ENCODE lzo
	,new_confirmed INTEGER   ENCODE az64
	,total_confirmed BIGINT   ENCODE az64
	,new_deaths INTEGER   ENCODE az64
	,total_deaths BIGINT   ENCODE az64
	,new_recovered INTEGER   ENCODE az64
	,total_recovered BIGINT   ENCODE az64
	,"time" TIMESTAMP WITHOUT TIME ZONE   ENCODE RAW
	,date DATE NOT NULL  ENCODE RAW
	,UNIQUE (country, date)
)
DISTSTYLE KEY
 DISTKEY (country)
 SORTKEY (
	date
	)
;
