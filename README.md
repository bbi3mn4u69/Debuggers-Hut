# Hotel Booking System

A professional Python application for managing hotel apartment bookings and guest reward points.

## Features

- **Apartment Booking Management**: Handle bookings for different apartment types
- **Reward Points System**: Track and award points to guests based on spending
- **Receipt Generation**: Generate formatted receipts for bookings
- **Input Validation**: Comprehensive validation for all user inputs

- **Error Handling**: Robust error handling with user-friendly messages

## Project Structure

```
assignment-1/
├── src/
│   └── hotel_booking/          # Main package
│       ├── __init__.py         # Package initialization
│       ├── main.py             # Application entry point
│       ├── config.py           # Configuration settings
│       ├── data_store.py       # Data management
│       ├── calculations.py     # Business logic
│       ├── io_prompts.py       # User input handling
│       └── receipt.py          # Receipt formatting
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_calculations.py
│   └── test_data_store.py
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd assignment-1
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Application

```bash
# From the project root
python -m hotel_booking.main

# Or if installed in development mode
python src/hotel_booking/main.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=hotel_booking

# Run specific test file
pytest tests/test_calculations.py
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Check code style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Configuration

The application uses a centralized configuration system in `src/hotel_booking/config.py`:

- **Apartments**: Available apartments and their nightly rates
- **Guests**: Initial guest data and points
- **Application Settings**: Hotel name, currency, date format

## API Reference

### Main Functions

#### `run_once() -> bool`

Execute one complete booking flow. Returns `True` if successful, `False` otherwise.

#### `run_interactive() -> None`

Run the application in interactive mode, allowing multiple bookings.

### Data Store Functions

#### `get_rate(apartment_id: str) -> float`

Get the nightly rate for an apartment. Returns `0.0` if apartment not found.

#### `add_points(guest_name: str, earned: int) -> int`

Add points to a guest's account. Returns the new total points.

#### `get_guest_points(guest_name: str) -> int`

Get current points for a guest. Returns `0` if guest not found.

### Calculation Functions

#### `compute_total_cost(rate: float, nights: int) -> float`

Calculate total cost for a booking.

#### `points_round_half_up(amount_aud: float) -> int`

Calculate reward points with half-up rounding.

## Development

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Run tests: `pytest`
4. Check code quality: `black`, `flake8`, `mypy`
5. Submit pull request

### Testing Strategy

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test module interactions
- **Error Handling**: Test error conditions and edge cases


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is for educational purposes as part of RMIT's Fundamental Programming course.

## Support

For questions or issues, please contact the development team or refer to the assignment documentation in the `assignment-details/` folder.
# Debuggers-Hut
