import reflex as rx

class SafeReflexComponent(rx.Component):
    """Base component to safely inject window-dependent code only on client."""
    def add_custom_code(self):
        return [
            """
            // Only define window variables if window is defined (client-side)
            if (typeof window !== 'undefined') {
                window.packageName = window.packageName || 'defaultPackageName';
            }
            """
        ]
