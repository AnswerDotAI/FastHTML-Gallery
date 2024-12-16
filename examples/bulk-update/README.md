# Bulk Update Example

This example demonstrates how to implement a bulk update interface using FastHTML and HTMX. Users can activate or deactivate multiple contacts simultaneously using checkboxes and see immediate feedback through a toast message.

## Features

- Checkbox-based selection of multiple contacts
- Bulk activation/deactivation of contacts
- Toast message feedback with fade-out animation
- Persistent state management
- ARIA-live announcements for accessibility

## Implementation Details

The example uses FastHTML's declarative syntax to create a simple interface that allows users to:
- View a list of contacts with their current status
- Select multiple contacts using checkboxes
- Update the status of selected contacts in bulk
- See immediate feedback through a toast message

The implementation showcases:
- FastHTML's form handling
- HTMX attributes for dynamic updates
- JavaScript integration for animations
- Proper state management
- Accessibility considerations

## Running the Example

```bash
python app.py
```

Visit `http://localhost:5001` to see the example in action.
