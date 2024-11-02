# Airflow Forex Data Pipeline

A robust data pipeline built with Apache Airflow 2.9.3 that fetches daily forex data (AUD/USD) from Alpha Vantage API, processes it using Polars, and stores it in PostgreSQL. The pipeline runs in a containerized environment using Docker.

## Features

- 📊 Daily forex data fetching from Alpha Vantage API
- 🐋 Fully containerized setup with Docker
- 🔄 Data processing using Polars (high-performance DataFrame library)
- 📬 Email notifications for pipeline success/failure
- 🗃️ PostgreSQL database for data storage
- 🎯 Monitoring with Redis and Flower

## Prerequisites

- Docker and Docker Compose installed
- Alpha Vantage API key ([Get it here](https://www.alphavantage.co/support/#api-key))
- Gmail account for SMTP notifications
- Python 3.8 or higher (if running locally)

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/alifnurhadi/airflow-postgres.git
cd airflow-postgres
```

2. Create a Gmail App Password:
   - Go to your Google Account settings
   - Navigate to Security > 2-Step Verification
   - At the bottom, select "App passwords"
   - Generate a new app password for "Mail"
   - Copy the generated password

3. Create `.env` file:
```env
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

4. Update `env.airflow` file with your Gmail credentials:
```env
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_USER=your.email@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=your_app_password_here
AIRFLOW__SMTP__SMTP_PORT=587
AIRFLOW__SMTP__SMTP_MAIL_FROM=your.email@gmail.com
```

## Installation & Deployment

1. Build the custom Dockerfile:
```bash
docker build -t custom-airflow-image .
```

2. Update the image name in `docker-compose.yaml`:
```yaml
image: custom-airflow-image
```

3. Initialize Airflow:
```bash
docker-compose up airflow-init
```

4. Start all services:
```bash
docker-compose up -d
```

## Project Structure

```
airflow-postgres/
├── dags/
│   └── forex_data_pipeline.py
├── logs/
├── plugins/
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env
└── env.airflow
```

## DAG Details

The forex data pipeline DAG (`updating_stock_data`) performs the following tasks:

1. Fetches AUD/USD forex data from Alpha Vantage API
2. Reformats the data using Polars
3. Performs data validation and error checking
4. Transforms and processes the data
5. Loads the data into PostgreSQL
6. Sends email notifications on success/failure

The DAG runs monthly and includes retry logic and error handling.

## Accessing Services

- Airflow UI: http://localhost:8080 (default credentials: airflow/airflow)
- Flower: http://localhost:5555
- PostgreSQL: localhost:5432
  - Database: myapp
  - Username: myapp
  - Password: myapp

## Monitoring

- Use the Airflow UI to monitor DAG runs and task status
- Access Flower dashboard to monitor Celery workers
- Check email notifications for pipeline success/failure
- View logs in the Airflow UI or in the `logs/` directory

## Troubleshooting

1. If the DAG fails to fetch data:
   - Verify your Alpha Vantage API key
   - Check API rate limits
   - Ensure network connectivity

2. If email notifications aren't working:
   - Verify SMTP settings in env.airflow
   - Check if the app password is correct
   - Ensure no firewall is blocking SMTP traffic

3. Database connection issues:
   - Ensure PostgreSQL container is running
   - Verify database credentials
   - Check network connectivity between containers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- GitHub: [@alifnurhadi](https://github.com/alifnurhadi)

## Acknowledgments

- [Apache Airflow](https://airflow.apache.org/)
- [Alpha Vantage API](https://www.alphavantage.co/)
- [Polars](https://pola.rs/)
