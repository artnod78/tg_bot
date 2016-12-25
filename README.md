Python class for Telegram bot
===================
All queries to the Telegram Bot API must be served over HTTPS and need to be presented in this form: `https://api.telegram.org/bot<token>/METHOD_NAME`. Like this for example:
```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getMe
```

TgBot
-------------
- **TgBot(token)** : Create new instance of TgBot. Each bot is given a unique authentication token when it is created. The token looks something like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.

- **get_Updates(param)** : Use this method to receive incoming updates using long polling ([wiki](https://en.wikipedia.org/wiki/Push_technology#Long_polling)). An Array of [Update](https://core.telegram.org/bots/api#update) objects is returned. **param** is a dictionnary of parameters.
Parameters      | Type			  | Required | Description
--------------- | --------------- | -------- | -----------
offset			| Integer		  | Optional | Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as [get_Updates](https://core.telegram.org/bots/api#getupdates) is called with an *offset* higher than its *update_id*. The negative offset can be specified to retrieve updates starting from *-offset* update from the end of the updates queue. All previous updates will forgotten.
limit			| Integer		  | Optional | Limits the number of updates to be retrieved. Values between 1—100 are accepted. Defaults to 100.
timeout			| Integer		  | Optional | Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
allowed_updates | Array of String | Optional | List the types of updates you want your bot to receive. For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. See [Update](https://core.telegram.org/bots/api#update) for a complete list of available update types. Specify an empty list to receive all updates regardless of type (default). If not specified, the previous setting will be used. <br><br> Please note that this parameter doesn't affect updates created before the call to the getUpdates, so unwanted updates may be received for a short period of time.

> **Notes**
 1. This method will not work if an outgoing webhook is set up.
 2 In order to avoid getting duplicate updates, recalculate offset after each server response.

- **send_Document(msg, path)**: Use this method to send general files. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
Parameters | Type	| Required | Description
---------- | ------ | -------- | -----------
msg		   | TgMsg  | Yes	   | TgMsg object. Extract *['message']['message_id']* for *reply_to_message_id* and extract *['message']['chat']['id']* for *chat_id*.
path	   | String | Yes	   | Local path of file to send.


- **send_Message(chat_id, text)**: Use this method to send text messages.
Parameters | Type			   | Required | Description
---------- | ----------------- | -------- | -----------
chat_id	   | Integer or String | Yes	  | Unique identifier for the target chat or username of the target channel (in the format `@channelusername`)
text	   | String			   | Yes	  | Text of the message to be sent.


- **get_Message()**: Return list of messages. Use *get_Updates* method.

- **get_MessageWithCommand()**: Return list of messages with one or more command present in message. Use *get_Updates* method and *TgMsg* object.

- **get_MessageWithDocument()**: Return list of messages with file in message. Use *get_Updates* method and *TgMsg* object.


- **get_File(file_id, full_path)**: Save *file_id* file at *full_path* path on bot server.

- **reply_Message(msg, text)**: Reply *text* to *reply_to_message_id*.

