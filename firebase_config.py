"""
Firebase Configuration Module
Connects to Firebase Firestore using the Admin SDK.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase():
    """
    Initialize the Firebase Admin SDK and return the Firestore client.

    Reads the path to the service account JSON file from the
    FIREBASE_CREDENTIALS environment variable.

    Returns:
        db: Firestore client instance, or None if initialization fails.
        error: Error message string, or None if initialization succeeds.
    """

    # Check if Firebase is already initialized
    if firebase_admin._apps:
        db = firestore.client()
        return db, None

    # Get the path to the Firebase service account key
    cred_path = os.getenv("FIREBASE_CREDENTIALS")

    if not cred_path:
        return None, (
            "FIREBASE_CREDENTIALS environment variable is not set. "
            "Please create a .env file with the path to your Firebase "
            "service account JSON key. See .env.example for reference."
        )

    if not os.path.exists(cred_path):
        return None, (
            f"Firebase service account file not found at: {cred_path}. "
            "Please check your FIREBASE_CREDENTIALS path in the .env file."
        )

    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db, None
    except Exception as e:
        return None, f"Failed to initialize Firebase: {str(e)}"
