# JBLSAvaliableChecker

Check a Jetbrains License Server is avaliable or not.

## Quick Start

- Install Python

- ```bash
  $ pip install -r requirements.txt
  ```

- ```bash
  $ uvicorn app.main:app --reload
  ```

## API Usage

- Path: `/api/fetch`

- Methods: `GET` or `POST`

- params:

  - `server`: The server url of the license server

- Return:

  - ```json
    {
      "available": bool,
      "message": "str",
      "data": {
        "release_ticket_data": {
          "action": "str",
          "confirmation_stamp": "str",
          "lease_signature": "str",
          "response_code": "str",
          "salt": "str",
          "server_lease": "str",
          "server_uid": "str",
          "validation_deadline_period": "str",
          "validation_period": "str"
        },
        "obtain_ticket_data": {
          "action": "str",
          "confirmation_stamp": "str",
          "lease_signature": "str",
          "message": "str",
          "prolongation_period": "str",
          "response_code": "str",
          "salt": "str",
          "server_lease": "str",
          "server_uid": "str",
          "validation_deadline_period": "str",
          "validation_period": "str"
        }
      }
    }
    ```

## Disclaimer

This program and its related documentation are provided for general informational purposes only. While we "str"ive to ensure the accuracy and completeness of the information, we make no representations or warranties of any kind, express or implied, regarding the accuracy, reliability, or completeness of the content. You use this program at your own risk.

We shall not be liable for any direct, indirect, incidental, special, or consequential damages arising from the use or inability to use this program, including but not limited to loss of data or profits, even if we have been advised of the possibility of such damages.

The use of this program may be subject to certain legal and regulatory requirements, and users are responsible for understanding and complying with applicable laws and regulations. We reserve the right to modify this disclaimer at any time without notice.
