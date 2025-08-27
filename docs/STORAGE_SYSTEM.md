# Storage System Documentation

## Overview

The Hotel Booking System uses an **in-memory storage system** to manage apartments and guest data. This document explains the current storage implementation and how to manage it.

## Current Storage Type

### **In-Memory Storage**

- **Type**: Python dictionaries stored in RAM
- **Persistence**: Data is lost when the application stops
- **Speed**: Very fast access and modifications
- **Use Case**: Development, testing, and simple applications

## Storage Structure

### 1. **Apartments Storage**

```python
_apartments: Dict[str, float] = {
    "U12swan": 95.0,      # Apartment ID -> Nightly Rate (AUD)
    "U209duck": 106.7,
    "U49goose": 145.2,
}
```

### 2. **Guests Storage**

```python
_guests_points: Dict[str, int] = {
    "Alyssa": 20,         # Guest Name -> Reward Points
    "Luigi": 32,
}
```

## Storage Management Tools

### 1. **Storage Manager Class** (`src/hotel_booking/storage_manager.py`)

The `StorageManager` class provides comprehensive tools to manage the storage:

#### **View Operations**

- `view_all_storage()` - View all data
- `view_apartments()` - View all apartments
- `view_guests()` - View all guests
- `get_storage_summary()` - Get statistics

#### **Search Operations**

- `search_apartments(term)` - Search apartments by ID
- `search_guests(term)` - Search guests by name

#### **Analytics**

- `get_top_guests(limit)` - Get guests with highest points
- `get_expensive_apartments(limit)` - Get most expensive apartments

#### **CRUD Operations**

- **Create**: `add_apartment()`, `add_guest()`
- **Read**: `view_apartments()`, `view_guests()`
- **Update**: `update_apartment_rate()`, `update_guest_points()`
- **Delete**: `delete_apartment()`, `delete_guest()`

#### **Bulk Operations**

- `clear_all_apartments()` - Remove all apartments
- `clear_all_guests()` - Remove all guests
- `clear_all_storage()` - Clear everything
- `reset_to_defaults()` - Reset to initial values

### 2. **Command Line Interface** (`storage_cli.py`)

A user-friendly CLI tool to manage storage:

```bash
python3 storage_cli.py
```

**Features:**

- Interactive menu system
- View storage summary and statistics
- Search and filter data
- Add, update, and delete items
- Bulk clear operations
- Confirmation prompts for destructive operations

## Usage Examples

### **Using the Storage Manager Programmatically**

```python
from hotel_booking.storage_manager import get_storage_manager

# Get the storage manager
storage = get_storage_manager()

# View current data
apartments = storage.view_apartments()
guests = storage.view_guests()

# Add new apartment
storage.add_apartment("U100luxury", 200.0)

# Update guest points
storage.update_guest_points("John", 150)

# Search for apartments
matches = storage.search_apartments("U1")

# Get top guests
top_guests = storage.get_top_guests(5)
```

### **Using the CLI Tool**

```bash
# Run the storage manager
python3 storage_cli.py

# Available options:
# 1. View storage summary
# 2. View all apartments
# 3. View all guests
# 4. View top guests by points
# 5. View most expensive apartments
# 6. Search apartments
# 7. Search guests
# 8. Add apartment
# 9. Update apartment rate
# 10. Delete apartment
# 11. Add guest
# 12. Update guest points
# 13. Delete guest
# 14. Clear storage
# 15. Exit
```

## Storage Synchronization

The system automatically synchronizes between the `StorageManager` and the legacy `data_store` functions:

- **Primary**: Uses `StorageManager` for all operations
- **Fallback**: Falls back to local dictionaries if `StorageManager` is unavailable
- **Consistency**: All data operations go through the same storage system

## Data Validation

The storage system includes comprehensive validation:

### **Apartment Validation**

- Apartment ID cannot be empty
- Rate must be positive
- Duplicate apartment IDs are prevented

### **Guest Validation**

- Guest name cannot be empty
- Points cannot be negative
- Duplicate guest names are prevented

## Storage Statistics

The system provides detailed statistics:

```python
summary = storage.get_storage_summary()
# Returns:
{
    "total_apartments": 3,
    "total_guests": 2,
    "total_points": 52,
    "total_apartment_value": 346.9,
    "average_rate": 115.63,
    "average_points": 26.0
}
```

## Limitations

### **Current In-Memory Storage**

1. **No Persistence**: Data is lost when application restarts
2. **Single Instance**: No sharing between multiple application instances
3. **Memory Limits**: Limited by available RAM
4. **No Backup**: No automatic backup or recovery

### **Future Improvements**

1. **Database Integration**: SQLite, PostgreSQL, or MongoDB
2. **File Persistence**: JSON, CSV, or custom file formats
3. **Cloud Storage**: AWS S3, Google Cloud Storage
4. **Caching**: Redis for high-performance caching
5. **Backup System**: Automatic backups and recovery

## Migration Path

To upgrade to persistent storage:

1. **Phase 1**: Add file-based persistence (JSON/CSV)
2. **Phase 2**: Implement SQLite database
3. **Phase 3**: Add cloud storage options
4. **Phase 4**: Implement caching layer

The current `StorageManager` interface is designed to be storage-agnostic, making future migrations seamless.

## Best Practices

1. **Always validate data** before storing
2. **Use the StorageManager** instead of direct dictionary access
3. **Handle errors gracefully** with try-catch blocks
4. **Log operations** for debugging and auditing
5. **Backup data regularly** when using persistent storage
6. **Test storage operations** thoroughly

## Troubleshooting

### **Common Issues**

1. **Data not persisting**: Normal for in-memory storage
2. **Import errors**: Ensure `storage_manager.py` is in the correct location
3. **Permission errors**: Check file permissions for CLI tool
4. **Memory issues**: Monitor memory usage with large datasets

### **Debug Commands**

```python
# Check storage status
storage = get_storage_manager()
print(storage.get_storage_summary())

# Verify data integrity
apartments = storage.view_apartments()
guests = storage.view_guests()
print(f"Found {len(apartments)} apartments and {len(guests)} guests")
```
