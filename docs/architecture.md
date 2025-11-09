# CA-Biositing Architecture Documentation

## Overview

CA-Biositing is a comprehensive geospatial bioeconomy platform for biodiversity data management and analysis, specifically focused on California biositing activities. The project combines ETL data pipelines, REST APIs, geospatial analysis tools, and web interfaces to support biodiversity research and conservation efforts. It processes data from Google Sheets into PostgreSQL databases and provides both programmatic and visual access to the data.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            EXTERNAL DATA SOURCES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Google Sheets API  │  External Datasets  │  Field Data Collection          │
└─────────────────────┬───────────────────────┬───────────────────────────────┘
                      │                       │
                      ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               ETL PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│  │   EXTRACT   │──▶│ TRANSFORM   │──▶│   VALIDATE  │──▶│    LOAD     │      │
│  │ Google      │   │ pandas      │   │ SQLModel    │   │ PostgreSQL  │      │
│  │ Sheets API  │   │ Processing  │   │ Validation  │   │ via Alembic │      │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘      │
│                                                                             │
│  Orchestrated by: Prefect + Docker                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA PERSISTENCE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    PostgreSQL Database                              │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │    │
│  │  │   Application   │  │    Prefect      │  │   Geospatial    │      │    │
│  │  │    Database     │  │   Metadata      │  │     Data        │      │    │
│  │  │   (biocirv_db)  │  │ (prefect_db)    │  │  (PostGIS ext)  │      │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        FastAPI REST API                             │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐     │    │
│  │  │   Data Access   │  │   Geospatial    │  │   Interactive    │     │    │
│  │  │   Endpoints     │  │    Queries      │  │  Documentation   │     │    │
│  │  │                 │  │                 │  │ (Swagger/OpenAPI)│     │    │
│  │  └─────────────────┘  └─────────────────┘  └──────────────────┘     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLIENT INTERFACES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌────────┐  │
│  │  Frontend Web   │  │      QGIS       │  │   Direct API    │  │ Custom │  │
│  │  Application    │  │   Geospatial    │  │   Integration   │  │ Clients│  │
│  │ (React/Next.js) │  │    Analysis     │  │                 │  │        │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Technology Stack

### Backend Infrastructure

- **Programming Language**: Python 3.12+
- **Database**: PostgreSQL 13+ with PostGIS extension
- **Database Migrations**: Alembic for schema versioning
- **Data Models**: SQLModel (combining SQLAlchemy + Pydantic)
- **API Framework**: FastAPI with automatic OpenAPI documentation
- **Data Processing**: pandas for transformation and analysis

### ETL Pipeline & Orchestration

- **Workflow Orchestration**: Prefect for pipeline management
- **Containerization**: Docker & Docker Compose for service orchestration
- **Data Sources**: Google Sheets API as primary data source
- **Data Validation**: Pydantic models for type safety and validation

### Frontend & Visualization

- **Frontend Framework**: React/Next.js (separate repository: `cal-bioscape-frontend`)
- **Geospatial Analysis**: QGIS integration for advanced spatial analysis
- **Package Management**: Node.js/npm for frontend dependencies

### Development & Deployment

- **Package Management**: Pixi for Python dependency management and task automation
- **Development Environment**: VS Code with dev containers
- **Code Quality**: Pre-commit hooks, pytest for testing
- **Version Control**: Git with submodules for frontend integration

### Cloud Infrastructure & Services

- **Google Cloud Platform**:
  - Google Sheets API for data ingestion
  - Google Cloud credentials management
  - Potential cloud deployment target
- **Database Hosting**: Containerized PostgreSQL (development), cloud SQL (production)
- **Container Registry**: For Docker image distribution

## Detailed Project Structure

### Namespace Package Architecture (PEP 420)

```
ca-biositing/
├── src/ca_biositing/                    # PEP 420 namespace package root
│   ├── datamodels/                      # Database models & configuration
│   │   ├── ca_biositing/datamodels/     # SQLModel definitions
│   │   │   ├── biomass.py               # Biomass entities & field samples
│   │   │   ├── geographic_locations.py  # Location data (GPS, addresses)
│   │   │   ├── experiments_analysis.py  # Experimental data models
│   │   │   ├── organizations.py         # Organization entities
│   │   │   ├── people_contacts.py       # People & contact information
│   │   │   ├── metadata_samples.py      # Sample metadata
│   │   │   ├── external_datasets.py     # External data integration
│   │   │   ├── config.py                # Model configuration
│   │   │   └── database.py              # Database connection setup
│   │   ├── tests/                       # Comprehensive test suite
│   │   └── pyproject.toml               # Independent package config
│   │
│   ├── pipeline/                        # ETL pipeline components
│   │   ├── flows/                       # Prefect flow definitions
│   │   ├── tasks/                       # Individual ETL tasks
│   │   └── pyproject.toml               # Pipeline-specific dependencies
│   │
│   └── webservice/                      # FastAPI REST API
│       ├── main.py                      # FastAPI application entry point
│       ├── routers/                     # API route definitions
│       ├── models/                      # API response models
│       └── pyproject.toml               # Web service dependencies
│
├── frontend/                            # Git submodule (separate repo)
│   └── (cal-bioscape-frontend)          # React/Next.js application
│
├── resources/                           # Deployment & infrastructure
│   ├── docker/                          # Docker configuration
│   │   ├── docker-compose.yml           # Service orchestration
│   │   ├── pipeline.dockerfile          # Multi-stage pipeline build
│   │   ├── .env.example                 # Environment template
│   │   └── create_prefect_db.sql        # Database initialization
│   └── prefect/                         # Prefect deployment config
│       ├── prefect.yaml                 # Deployment definitions
│       ├── deploy.py                    # Automated deployment script
│       └── run_prefect_flow.py          # Master flow orchestration
│
├── docs/         
│   ├── README.md                        # Main ReadMe file
│   ├── Architecture.md                  # Project architecture [This file]
│   ├── api/                             # Folder for api docs
│   └── pipeline/  
│       ├── DOCKER_WORKFLOW.md           # Docker deployment guide
│       ├── PREFECT_WORKFLOW.md          # Prefect orchestration guide
│       ├── ETL_WORKFLOW.md              # ETL development guide
│       ├── ALEMBIC_WORKFLOW.md          # Database migration guide
│       └── GCP_SETUP.md                 # Google Cloud setup
│
├── alembic/                             # Database migration management
│   ├── versions/                        # Migration scripts
│   └── env.py                           # Alembic environment config
│
├── tests/                               # Integration tests
├── .devcontainer/                       # Development container setup
├── .github/                             # CI/CD workflows
├── .vscode/                             # IDE configuration
├── pixi.toml                            # Project dependencies & tasks
└── pixi.lock                            # Dependency lock file
```

## Data Flow Architecture

### 1. Data Ingestion (Extract)

```
Google Sheets ──API──▶ Python ETL Pipeline
     │                        │
     ├── Biomass Data         ├── Google Sheets API Client
     ├── Location Data        ├── Authentication (credentials.json)
     ├── Sample Data          └── Rate Limiting & Error Handling
     └── Experimental Data
```

### 2. Data Processing (Transform)

```
Raw Data ──pandas──▶ Cleaned Data ──SQLModel──▶ Validated Data
    │                     │                         │
    ├── Data Cleaning     ├── Normalization         ├── Type Validation
    ├── Format Conversion ├── Standardization       ├── Business Rules
    └── Quality Checks    └── Enrichment           └── Constraint Checking
```

### 3. Data Persistence (Load)

```
Validated Data ──Alembic──▶ PostgreSQL Database
       │                         │
       ├── Schema Validation     ├── ACID Transactions
       ├── Batch Processing      ├── Geospatial Extensions
       └── Conflict Resolution   └── Performance Optimization
```

### 4. Data Access & Consumption

```
PostgreSQL ──SQLModel──▶ FastAPI ──HTTP/JSON──▶ Client Applications
     │                     │                        │
     ├── Query Optimization├── REST Endpoints       ├── Web Frontend
     ├── Geospatial Queries├── OpenAPI Documentation├── QGIS Integration
     └── Aggregations      └── Type-safe Responses └── Direct API Access
```

## Service Architecture (Docker Compose)

### Development Environment Services

1. **PostgreSQL Database** (`db`)

   - **Image**: PostgreSQL 13+
   - **Purpose**: Primary data storage for application and Prefect metadata
   - **Databases**:
     - `biocirv_db` - Application data
     - `prefect_db` - Prefect workflow metadata
   - **Extensions**: PostGIS for geospatial data support
   - **Port**: 5432 (configurable)
   - **Persistence**: Docker volumes for data durability

2. **Database Migration** (`setup-db`)

   - **Purpose**: One-time schema initialization and upgrades
   - **Tool**: Alembic for version-controlled migrations
   - **Dependency**: Waits for database health check
   - **Execution**: Runs on service startup

3. **Prefect Server** (`prefect-server`)

   - **Purpose**: Workflow orchestration and monitoring
   - **Port**: 4200 (Web UI and API)
   - **Features**:
     - Flow scheduling and execution
     - Real-time monitoring dashboard
     - Workflow history and logging
     - Work pool management

4. **Prefect Worker** (`prefect-worker`)
   - **Purpose**: Execute flow runs from work pools
   - **Features**:
     - Process-based task execution
     - Access to Google Cloud credentials
     - Connection to application database
     - Automatic retry and error handling

### Network Architecture

- **Internal Network**: `prefect-network` bridge network
- **Service Discovery**: Container names as hostnames
- **External Access**: Mapped ports for UI and database access

## Data Models & Entities

### Core Domain Models

#### Biomass Models

- **Biomass**: Core biomass entity with classification
- **FieldSample**: Field collection metadata and measurements
- **BiomassType**: Lookup table for biomass categories
- **BiomassAvailability**: Seasonal and quantitative availability data
- **BiomassQuality**: Quality metrics and attributes
- **BiomassPrice**: Pricing information and market data
- **HarvestMethod**: Collection methodology lookup

#### Geographic Models

- **GeographicLocation**: Primary location entity (can be anonymized)
- **StreetAddress, City, County, State**: Hierarchical location components
- **FIPS**: Federal Information Processing Standards codes
- **LocationResolution**: Resolution types (GPS coordinates, county-level, etc.)

#### Research Models

- **ExperimentAnalysis**: Experimental design and results
- **MetadataSamples**: Sample processing and metadata
- **SpecificAnalysisResults**: Detailed analysis outcomes
- **ExternalDatasets**: Integration with external data sources

#### Organizational Models

- **Organizations**: Research institutions and companies
- **PeopleContacts**: Researchers and contact information
- **User**: System user management and permissions

## Google Cloud Integration

### Google Sheets API Integration

```
Google Cloud Platform
├── Service Account Authentication
│   ├── credentials.json (local development)
│   └── IAM roles for Sheets API access
├── Google Sheets API v4
│   ├── Read access to research data sheets
│   ├── Rate limiting and quota management
│   └── Error handling and retry logic
└── Data Security
    ├── OAuth 2.0 authentication flow
    ├── API key management
    └── Access logging and monitoring
```

### Authentication Flow

1. **Service Account**: Created in Google Cloud Console
2. **Credentials**: Downloaded as `credentials.json`
3. **API Access**: Sheets API enabled for project
4. **Permissions**: Service account granted read access to target sheets
5. **ETL Integration**: Pipeline authenticates and extracts data

### Cloud Deployment Considerations

- **Google Cloud SQL**: PostgreSQL managed database service
- **Google Cloud Run**: Containerized API deployment
- **Google Cloud Build**: CI/CD pipeline for automated deployment
- **Google Cloud Storage**: Backup and archival storage
- **Google Cloud Monitoring**: Application and infrastructure monitoring

## API Architecture (FastAPI)

### REST API Design

```
/api/v1/
├── /biomass/                    # Biomass data endpoints
│   ├── GET /                    # List biomass entities
│   ├── GET /{id}                # Get specific biomass
│   └── GET /{id}/samples        # Get associated samples
├── /locations/                  # Geographic data endpoints
│   ├── GET /                    # List locations
│   ├── GET /{id}                # Get specific location
│   └── GET /search              # Geospatial search
├── /experiments/                # Research data endpoints
├── /organizations/              # Organization endpoints
└── /health                      # System health checks
```

### API Features

- **Auto-generated Documentation**: Swagger UI at `/docs`
- **Type Safety**: Pydantic models for request/response validation
- **Geospatial Queries**: PostGIS integration for spatial operations
- **Pagination**: Efficient handling of large datasets
- **Filtering & Search**: Query parameters for data filtering
- **CORS Support**: Cross-origin resource sharing for web frontend

## Frontend Architecture

### Frontend Repository Integration

- **Repository**: `sustainability-software-lab/cal-bioscape-frontend`
- **Integration**: Git submodule in `frontend/` directory
- **Technology**: React/Next.js with TypeScript
- **Package Management**: npm for Node.js dependencies
- **Development**: Hot reloading and development server

### Frontend-Backend Communication

```
Frontend (React) ──HTTP/REST──▶ Backend API (FastAPI)
     │                               │
     ├── Data Visualization          ├── JSON Responses
     ├── Interactive Maps            ├── Geospatial Data
     ├── Search & Filtering          ├── Query Processing
     └── User Interface              └── Authentication
```

## Development Workflow & Environment Management

### Pixi Environment Configuration

```
Environments:
├── default: General development, testing, pre-commit
├── gis: QGIS and geospatial analysis tools
├── etl: ETL pipeline (used in Docker containers)
├── webservice: FastAPI web service
├── frontend: Node.js/npm for frontend development
├── py312/py313: Python version-specific environments
├── docs: To generate docs using MKdocs
```

### Key Development Tasks

- **Service Management**: Start/stop/monitor Docker services
- **Database Operations**: Migrations, health checks, direct access
- **ETL Operations**: Deploy and run data pipelines
- **Testing**: Comprehensive test suites with coverage
- **Code Quality**: Pre-commit hooks, linting, formatting

## Deployment & Operations

### Container Orchestration

- **Development**: Docker Compose for local services
- **Production**: Kubernetes or cloud container services
- **Image Building**: Multi-stage Dockerfiles for optimization
- **Environment Configuration**: Environment variables and secrets

### Database Management

- **Schema Versioning**: Alembic migrations for schema changes
- **Backup Strategy**: Automated database backups
- **Performance Monitoring**: Query optimization and indexing
- **Geospatial Optimization**: PostGIS spatial indexes

### Monitoring & Observability

- **Application Monitoring**: Health checks and metrics
- **Pipeline Monitoring**: Prefect UI for workflow visibility
- **Database Monitoring**: PostgreSQL performance metrics
- **Log Aggregation**: Centralized logging for troubleshooting

## Security Considerations

### Data Security

- **Authentication**: Google Cloud service account authentication
- **API Security**: CORS configuration and rate limiting
- **Database Security**: Connection encryption and access controls
- **Credential Management**: Secure storage of API keys and passwords

### Privacy & Compliance

- **Data Anonymization**: Geographic location anonymization options
- **Access Controls**: Role-based access to sensitive data
- **Audit Logging**: Tracking of data access and modifications
- **Data Retention**: Policies for data lifecycle management

## Scalability & Performance

### Database Optimization

- **Indexing Strategy**: Optimized indexes for common queries
- **Geospatial Performance**: PostGIS spatial indexes and optimization
- **Query Optimization**: Efficient SQL generation via SQLModel
- **Connection Pooling**: Database connection management

### API Performance

- **Caching Strategy**: Redis for frequently accessed data
- **Pagination**: Efficient handling of large result sets
- **Async Processing**: FastAPI async support for I/O operations
- **Rate Limiting**: API throttling for resource protection

### Pipeline Scalability

- **Parallel Processing**: Prefect concurrent task execution
- **Batch Processing**: Efficient bulk data operations
- **Error Recovery**: Automatic retry and failure handling
- **Resource Management**: Memory and CPU optimization

## Future Architecture Considerations

### Microservices Evolution

- **Service Decomposition**: Breaking monolith into focused services
- **API Gateway**: Centralized API management and routing
- **Event-Driven Architecture**: Asynchronous communication patterns
- **Service Mesh**: Advanced networking and observability

### Cloud-Native Enhancements

- **Serverless Functions**: Google Cloud Functions for specific tasks
- **Managed Services**: Cloud SQL, Cloud Storage, Cloud Monitoring
- **Auto-scaling**: Horizontal scaling based on demand
- **Multi-region Deployment**: Geographic distribution for performance

### Advanced Analytics

- **Data Warehouse**: BigQuery integration for analytics
- **Machine Learning**: ML pipelines for predictive analytics
- **Real-time Processing**: Stream processing for live data
- **Data Lake**: Large-scale data storage and processing

This architecture supports the project's mission of providing a robust, scalable platform for California biodiversity data management while maintaining flexibility for future enhancements and cloud deployment.
