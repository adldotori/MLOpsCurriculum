## Give Money

> PUT /user/<id\:int>/money

### Parameter

| Name      | Type | Description         | Required |
| --------- | ---- | ------------------- | -------- |
| target_id | int  | 돈을 받는 유저의 id | V        |
| money     | int  | 전달할 금액         | V        |

### Response

| Name    | Type | Description | Required |
| ------- | ---- | ----------- | -------- |
| success | bool | 성공 여부   | V        |
