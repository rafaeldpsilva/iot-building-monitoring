# Energy Management API

This is a Flask-based API for managing tokens, energy data, IoT devices, batteries, and demand response services in an energy management system.

## Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Flask
- Flask-CORS

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/energy-management-api.git
   cd energy-management-api
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a configuration file or environment variables as required by `utils.get_config()` to set the necessary configurations, including the application's port.

## Running the Application

To run the application, execute the following command in the project directory:

```bash
python main.py
```

By default, the application will run on `http://0.0.0.0:<configured-port>`.

## API Endpoints

### General Endpoints

- `GET /` - Check if the server is online.

### Token Management Endpoints

- `GET /tokens` - Get the list of tokens.
- `POST /tokens/generate` - Generate a new token.
- `POST /tokens/check` - Check the validity of a token.
- `POST /tokens/save` - Save a token.
- `POST /tokens/revoke` - Revoke a token.

### Energy Data Endpoints

- `GET /overview` - Get an overview of historic and forecasted energy data.
- `GET /historic` - Get historic energy consumption data for the last day.
- `POST /historic/interval` - Get energy consumption and generation data for a specific interval.

### IoT Device Endpoints

- `GET /iots` - Get a list of IoT devices.
- `POST /iot/historic` - Get historic data for a specific IoT device.

### Battery Endpoints

- `GET /batteries` - Get a list of batteries.
- `GET /batteries/historic` - Get historic battery data for the last day.
- `POST /batteries/charge` - Charge a battery.

### Energy Endpoints

- `GET /energy/now` - Get current energy consumption and generation.
- `GET /energy/totalpower` - Get total power consumption.
- `GET /energy/consumption` - Get energy consumption data.
- `GET /energy/generation` - Get energy generation data.
- `GET /energy/flexibility` - Get energy flexibility data.

### Forecast Endpoints

- `GET /forecast/consumption` - Get forecasted energy consumption.
- `GET /forecast/generation` - Get forecasted energy generation.
- `GET /forecast/flexibility` - Get forecasted energy flexibility.

### Demand Response Endpoints

- `POST /invitation/get` - Get a demand response invitation.
- `GET /invitation/unanswered` - Get unanswered demand response invitations.
- `GET /invitation/answered` - Get answered demand response invitations.
- `POST /invitation/answer` - Answer a demand response invitation.
- `POST /invitation/send` - Send a demand response invitation.
- `GET /invitation/auto` - Get auto-answer configuration for invitations.
- `POST /invitation/auto` - Set auto-answer configuration for invitations.

### Division Endpoints

- `GET /divisions` - Get a list of divisions.
- `POST /divisions/create` - Create a new division.
- `POST /divisions/update` - Update an existing division.
- `POST /divisions/acstatus` - Get AC status of a division.

### Production Endpoint

- `GET /production/breakdown` - Get production breakdown data.

### Utility Endpoints

- `GET /audit/check` - Perform an audit check.
- `POST /benefit` - Add benefit data for an IoT device.
- `GET /benefit/historic` - Get historic benefit data.
