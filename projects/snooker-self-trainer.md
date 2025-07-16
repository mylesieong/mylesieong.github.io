---
layout: default
title: Snooker Self-Trainer - Myles Ieong
---

# Snooker Self-Trainer

**Duration**: 2024 - Present  
**Technologies**: Kotlin Multiplatform, Compose Multiplatform, SQLDelight, SQLite  
**Role**: Full-stack Mobile Developer

## Overview

A comprehensive snooker training assistant app designed to help players improve their skills through structured drills, personalized training plans, and detailed performance tracking. The app provides a rich library of drills covering all cue sport skills with set-based tracking similar to fitness apps.

![Snooker Self-Trainer App](/assets/images/snooker.jpg)

## Key Features

- **Structured Drill Practice**: 100+ drills with set/reps tracking and progress monitoring
- **Personalized Training Plans**: AI-driven training schedules with automatic progression and daily recommendations
- **Self-Assessment Exams**: Customizable shot sequences with detailed performance analysis
- **Comprehensive Knowledge Base**: Interactive handbook with snooker rules, techniques, and advanced concepts
- **Game Performance Tracking**: Match analysis with detailed statistics and improvement tracking
- **Multi-step Onboarding**: Personalized plan creation based on skill level (Beginner/Intermediate/Advanced)

## App Screenshots

![Snooker App - Dashboard](/assets/images/snooker-1.jpg)
![Snooker App - Training Plan](/assets/images/snooker-2.jpg)
![Snooker App - Drills](/assets/images/snooker-3.jpg)
![Snooker App - Drill Details](/assets/images/snooker-4.jpg)
![Snooker App - Performance Tracking](/assets/images/snooker-5.jpg)

## Technical Details

- **Frontend**: Kotlin Multiplatform + Compose Multiplatform (shared UI for Android/iOS)
- **Backend**: Local SQLite database with SQLDelight for persistence
- **Navigation**: Compose Navigation for seamless screen transitions
- **Architecture**: Clean architecture with MVVM pattern
- **Deployment**: Native mobile apps for Android and iOS

## Technical Implementation

The app features a sophisticated architecture with:
- **15+ Screens**: Complete user journey from onboarding to advanced training
- **Data Models**: Comprehensive enums for drills/exams, structured handbook content, and detailed record tracking
- **Offline-First**: All content accessible without internet connection
- **Calendar Integration**: Color-coded training events and progress tracking
- **Performance Analytics**: Detailed statistics on training hours, completion rates, and skill progression

## Challenges & Solutions

**Challenge**: Creating a cross-platform mobile app with complex navigation and data persistence
**Solution**: Leveraged Kotlin Multiplatform and Compose Multiplatform to share 90%+ of code between Android and iOS while maintaining native performance and UI standards.

**Challenge**: Designing an intuitive interface for complex training workflows
**Solution**: Implemented a drawer-based navigation system with clear visual hierarchy and progressive disclosure of features.

**Challenge**: Managing complex training data and progress tracking
**Solution**: Built a robust SQLite-based data layer with SQLDelight for type-safe database operations and efficient querying.

## App Store Links

- **Google Play**: [Snooker Self-Trainer on Google Play](https://play.google.com/store/apps/details?id=com.municornio.app.snookerselftrainer)
- **App Store**: [Snooker Self-Trainer on App Store](https://apps.apple.com/us/app/snooker-self-trainer/id6747923097)

## Additional Links

- **GitHub Repository**: [Link to repo]
- **Documentation**: [Link to technical docs if available]

---

[← Back to Projects](/projects) | [Home](/) 