# Fit Market Calculator

This is a tool for Eve Online, an internet spaceship game.

Fits are collections of items. Typically, this means a ship and its component parts.
Market data is gathered from regions of space within the game. This application focuses on regions with markets of significance.

## Architecture
Lambda and DynamoDB were chosen for two reasons:
1) They do not incur costs when not actively processing requests except for near-zero storage costs.
2) The main developer on this project wanted to learn these tools.

