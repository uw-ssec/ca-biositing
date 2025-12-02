# CA Biositing API Documentation

This document provides an overview of the CA Biositing REST API endpoints and
their usage.

## Overview

The CA Biositing API is a FastAPI-based REST API that provides access to
bioeconomy data including biomass, experiments, samples, locations, and
products. The API follows RESTful conventions and provides automatic OpenAPI
documentation.

## Base URL

- **Development**: `http://localhost:8000`
- **API Version**: `v1`

## Interactive Documentation

Once the server is running, interactive documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Authentication

Currently, the API does not require authentication. Authentication can be added
in the future using the prepared middleware structure.

## CORS Configuration

CORS is configured to allow requests from common frontend development ports:

- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- `http://localhost:8080` (Alternative port)

## Common Patterns

### Pagination

All list endpoints support pagination using query parameters:

```
GET /v1/biomass?skip=0&limit=50
```

**Parameters**:

- `skip` (integer, min: 0, default: 0): Number of records to skip
- `limit` (integer, min: 1, max: 100, default: 50): Maximum records to return

**Response Format**:

```json
{
  "items": [...],
  "pagination": {
    "total": 100,
    "skip": 0,
    "limit": 50,
    "returned": 50
  }
}
```

### Error Responses

The API uses standard HTTP status codes and returns errors in a consistent
format:

**404 Not Found**:

```json
{
  "detail": "Biomass with ID 999 not found"
}
```

**422 Validation Error**:

```json
{
  "detail": "Validation error",
  "errors": [...]
}
```

**500 Internal Server Error**:

```json
{
  "detail": "Internal server error",
  "error": "Error message"
}
```

## Endpoints

### Root Endpoints

#### Get API Information

```
GET /
```

Returns basic API information including version and links to documentation.

**Response**:

```json
{
  "message": "CA Biositing API",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/v1/health"
}
```

#### Health Check (Legacy)

```
GET /hello
```

Simple hello world endpoint for testing.

### Health Check

#### Check API Health

```
GET /v1/health
```

Returns the health status of the API and its dependencies.

**Response**:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "database": "connected"
}
```

### Biomass Endpoints

#### List Biomass Entries

```
GET /v1/biomass
```

Get a paginated list of all biomass entries.

**Query Parameters**: `skip`, `limit` (see Pagination)

**Response**: Paginated list of biomass entries

#### Get Biomass by ID

```
GET /v1/biomass/{biomass_id}
```

Get a specific biomass entry by ID.

**Response**:

```json
{
  "biomass_id": 1,
  "biomass_name": "Corn Stover",
  "primary_product_id": 1,
  "taxonomy_id": 2,
  "biomass_type_id": 1,
  "biomass_notes": "Agricultural residue"
}
```

#### Create Biomass

```
POST /v1/biomass
```

Create a new biomass entry.

**Request Body**:

```json
{
  "biomass_name": "Corn Stover",
  "primary_product_id": 1,
  "taxonomy_id": 2,
  "biomass_type_id": 1,
  "biomass_notes": "Agricultural residue"
}
```

**Response**: Created biomass entry (201 Created)

#### Update Biomass

```
PUT /v1/biomass/{biomass_id}
```

Update an existing biomass entry. All fields are optional for partial updates.

**Request Body**:

```json
{
  "biomass_name": "Updated Name",
  "biomass_notes": "Updated notes"
}
```

**Response**: Updated biomass entry

#### Delete Biomass

```
DELETE /v1/biomass/{biomass_id}
```

Delete a biomass entry.

**Response**:

```json
{
  "message": "Biomass 1 deleted successfully"
}
```

### Experiment Endpoints

#### List Experiments

```
GET /v1/experiments
```

Get a paginated list of all experiments.

**Query Parameters**: `skip`, `limit` (see Pagination)

#### Get Experiment by ID

```
GET /v1/experiments/{experiment_id}
```

Get a specific experiment by ID.

#### Create Experiment

```
POST /v1/experiments
```

Create a new experiment.

**Request Body**:

```json
{
  "exper_uuid": "unique-id",
  "gsheet_exper_id": 1,
  "exper_description": "Biomass analysis experiment",
  "exper_start_date": "2024-01-01",
  "exper_duration": 30,
  "analysis_type_id": 1
}
```

#### Update Experiment

```
PUT /v1/experiments/{experiment_id}
```

Update an existing experiment.

#### Delete Experiment

```
DELETE /v1/experiments/{experiment_id}
```

Delete an experiment.

### Field Sample Endpoints

#### List Samples

```
GET /v1/samples
```

Get a paginated list of all field samples.

#### Get Sample by ID

```
GET /v1/samples/{sample_id}
```

Get a specific field sample by ID.

#### Create Sample

```
POST /v1/samples
```

Create a new field sample.

**Required Fields**:

- `biomass_id`: Reference to biomass
- `sample_name`: Name of the sample

#### Update Sample

```
PUT /v1/samples/{sample_id}
```

Update an existing field sample.

#### Delete Sample

```
DELETE /v1/samples/{sample_id}
```

Delete a field sample.

### Location Endpoints

#### List Locations

```
GET /v1/locations
```

Get a paginated list of all geographic locations.

#### Get Location by ID

```
GET /v1/locations/{location_id}
```

Get a specific location by ID.

#### Create Location

```
POST /v1/locations
```

Create a new geographic location.

#### Update Location

```
PUT /v1/locations/{location_id}
```

Update an existing location.

#### Delete Location

```
DELETE /v1/locations/{location_id}
```

Delete a location.

### Product Endpoints

#### List Products

```
GET /v1/products
```

Get a paginated list of all primary products.

#### Get Product by ID

```
GET /v1/products/{product_id}
```

Get a specific product by ID.

#### Create Product

```
POST /v1/products
```

Create a new primary product.

**Request Body**:

```json
{
  "primary_product_name": "Biochar"
}
```

#### Update Product

```
PUT /v1/products/{product_id}
```

Update an existing product.

#### Delete Product

```
DELETE /v1/products/{product_id}
```

Delete a product.

## Development

### Running the API

Using Pixi (recommended):

```bash
pixi run start-webservice
```

Using uvicorn directly:

```bash
cd src
uvicorn ca_biositing.webservice.main:app --reload
```

### Running Tests

```bash
pytest src/ca_biositing/webservice/tests/ -v
```

### Environment Variables

The API can be configured using environment variables with the `API_` prefix:

- `API_CORS_ORIGINS`: Comma-separated list of allowed CORS origins
- `DATABASE_URL`: PostgreSQL connection URL (from datamodels package)
- `ECHO_SQL`: Enable SQL query logging (from datamodels package)

Example `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/ca_biositing
ECHO_SQL=false
API_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## Architecture

The webservice follows a layered architecture:

1. **Endpoints** (`v1/endpoints/`): Handle HTTP requests/responses
2. **Services** (`services/`): Business logic and data operations
3. **Schemas** (`schemas/`): Pydantic models for validation
4. **Dependencies** (`dependencies.py`): Dependency injection
5. **Config** (`config.py`): Application configuration

This separation ensures:

- Clean code organization
- Easy testing with mocks
- Reusable business logic
- Type safety throughout

## Future Enhancements

Potential improvements for future development:

1. **Authentication**: Add OAuth2/JWT authentication
2. **Rate Limiting**: Implement request throttling
3. **Caching**: Add Redis caching for frequently accessed data
4. **Search**: Add full-text search capabilities
5. **Filtering**: Enhanced filtering options for list endpoints
6. **Batch Operations**: Support bulk create/update/delete
7. **Relationships**: Expand endpoints to include related data
8. **WebSockets**: Real-time data updates
9. **GraphQL**: Alternative API interface
10. **API Versioning**: Support multiple API versions

## Support

For issues, questions, or contributions, please visit:

- **Repository**: https://github.com/uw-ssec/ca-biositing
- **Issues**: https://github.com/uw-ssec/ca-biositing/issues
