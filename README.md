# Mail manager

This is a simple script that managers your mail. Some if its functions include:

```
1. Checks for new mails
2. Sends mails
3. Show last E-mail
4. Show all drafts
```

## Usage

You can manually login each time you run the program. Fill in the correct creditentials
when prompted.
However, if you wish to automatically login each time, you could simply remove the code
where the input is promted and add your creditentials in the

`def mail_login(email='[EMAIL]', passwd='[PASSWORD]')` function.

NOTE : For `imaplib` to be able to login to your account, You should enable `Less secure apps`
on your google account. Read more about it [here](https://support.google.com/a/answer/6260879?hl=en)
