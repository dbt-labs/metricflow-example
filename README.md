# MetricFlow Example Repo

This repository provides an example of an end-to-end deployment of MetricFlow. You will need to have the following installed on your device:

* [Docker](https://www.docker.com/products/docker-desktop/)
* [MetricFlow](https://github.com/transform-data/metricflow)
* [PostgreSQL](https://www.postgresql.org/download/)
* [Python 3.9](https://www.python.org/downloads/)
* [Metabase](https://www.metabase.com/docs/latest/operations-guide/running-metabase-on-docker.html)

## Installation

Download this repository (Add link)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install metricflow.

```bash
pip install metricflow
```

Navigate to metricflow/local-data-warehouses/postgresql using
```bash
cd metricflow/local-data-warehouses/postgresql
```
and then run
```bash
docker-compose up
```

Run 
```bash
mf setup
```

It will ask you to enter your data warehouse dialect. Enter postgresql. 

A template file will be created. If you've run this before, it will say "a template config already exists in \<location>. 

Run 
```bash
mf tutorial
```

Navigate to the template file created earlier and fill it out with the following
```yml
dwh_schema: 'transform'
model_path: /Users/{username}/.metricflow/sample_models  # Path to directory containing defined models (Leave until after DWH setup). Specify the username for your system
email: ''  # Optional
dwh_dialect: postgresql
dwh_host: '127.0.0.1'  # Host name
dwh_port: '5432'
dwh_user: 'metricflow'  # Username for the data warehouse
dwh_password: 'metricflowing'  # Password associated with the provided user
dwh_database: 'metricflow'
```

## Creating a Materialization

MetricFlow supports PostgreSQL which means you can use it without having to set up a connection to your own data warehouse. We can access the sample data that's loaded in the tutorial by creating a materialization. 

More information about materializations in MetricFlow can be found [here](https://docs.transform.co/docs/metricflow/reference/materializations/#what-are-materializations-in-metricflow).

To create the materialization, navigate to the model_path specified in the previous step and save [this file](https://drive.google.com/file/d/1hVJUSauvap91Ihe18qqR7xi0YEfWmOfq/view?usp=sharing) to that location. You can also create the materialization.yaml file manually and fill it out with the following:
```yml
materialization:
  name: example_materialization # name your materialization. this will be the table name written in your data warehouse.
  description: test description # add an optional description.
  metrics: # list all the metrics you want to materialize in your materialization. all metrics must be defined in your model.
    - cancellations
    - cancellation_rate
    - revenue_usd
    - cancellations_mx
    - transaction_usd_na
    - transaction_usd_l7d_mx
    - transaction_usd_mtd
    - transaction_usd_na_l7d
    - transaction_amount_usd
    - transactions
    - quick_buy_amount_usd
    - new_customers

  dimensions: # list all corresponding dimensions you want to include for these metrics. these must all be defined in your data sources. these dimensions must be shared across all metrics in your materialization.
    - ds

  destination_table: transform.example_materialization # The materialization will be written to this destination.

# Optional destinations:
# Materializations always write to the datawarehouse. You can specify additional optional destinations. Check the documentation for a complete list of destinations.
  destinations:
    - location: DW
      format: WIDE

 ```

Then, run
```
mf materialize --materialization-name example_materialization
```

You can run mf list-materializations to verify that the materialization was created successfully. 

You can also query this materialization using the PostgreSQL CLI by running
```
 psql -s mydb
```

## Using MetricFlow with Metabase
You can navigate to [localhost:3000](localhost:3000) to access Metabase.

You can also open it from the Containers section in Docker

![](https://drive.google.com/file/d/1S1ZAnx3_5PfwsXXBHvbsuSSMTn6qz_0e/view?usp=sharing)

Enter your login information when prompted. 
To add your data, select PostgreSQL and fill out the fields with the following:\
**Display name**: ExampleDB\
**Host**: 127.0.0.1\
**Port**: 5432\
**Database name**: \<Container ID> (To obtain this, run 'docker ps' and copy the Container ID that corresponds to the Postgres image)  
**Username**: metricflow\
**Password**: metricflowing

Once Metabase is open, using the Browse data tab on the left, navigate to ExampleDB/transform /\<Materialization Name>

After you've navigated to the correct table, you can create visualizations using the Visualizations button on the bottom-left. You can also create a dashboard and add your visualizations there.

![](https://drive.google.com/file/d/1XYNnk4upLyv24HIfIeUNshiJ8s8B3SIq/view?usp=sharing)

Pictures of Examples

## Using MetricFlow with Python
Explainer and link to Jupyter Notebook

## Additional Resources
[Metabase tutorial](https://www.metabase.com/learn/getting-started/getting-started.html)