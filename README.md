# Channel Chat Hub/HubChatLive

## Introduction
Channel Chat Hub/HubChatLive is an interactive chat platform connecting users worldwide. This application allows users to send text messages via POST requests, with the latest 15 messages appearing in the response.

## Features
- **Real-Time Messaging**: Send and receive messages in real-time.
- **Privacy Notice**: Keep chat private as there's no encryption. Avoid sending sensitive content.
- **Admin Communication**: Special room (`admin-ef1fedf5d3`) for messaging admins. Do not share messages from the admin room.

## Usage

### Sending Messages
Send messages in the following format:
```json
{
  "nickname": "YourNickname",
  "text": "Your Message"
}
```
If you need to change your nickname, send it via the nickname field.

### Receiving Messages
Messages are received in an array, showing up to the 15 most recent messages. For example:

```json
[
  {
    "nickname": "Anon",
    "text": "Old message",
    "date": "2023-11-13T10:09:40.162697"
  },
  // More messages here
]
```
Messages will be displayed in the view, with newer messages at the bottom.

### Message Formatting and Instructions
You can send messages with specific instructions, like generating an image or highlighting a message. For example:

```json
{
  "chat": "test",
  "nickname": "Bob",
  "text": "the cat",
  "instruction": "generate image: Black cat hiding in soup"
}
```
Use the instruction field for special message formats or actions.

### Getting Started
Follow the standard installation and running instructions as outlined in the previous sections of this README.

### Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.