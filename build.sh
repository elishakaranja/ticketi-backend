#!/usr/bin/env bash
# Build script for Ticketi backend on Render

set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Optional: Seed database (comment out after first deploy)
# python seed_kenya_events.py
