# Video Ingestion Module

## Purpose

The Video Ingestion module is responsible for reading frames from a video source (camera, RTSP stream, or video file) and providing them to downstream AI modules.

## Responsibilities

- Connect to video sources
- Read frames continuously
- Handle reconnection
- Provide frame metadata
- Report stream status

## Downstream Consumers

- Detection Module
- Tracking Module