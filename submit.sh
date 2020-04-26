#!/bin/bash

echo "Zipping Submission Folder"
zip -r evan_chong_9769I.zip submission

echo "Uploading Submission Zipfile"
/opt/azcopy_linux_amd64_10.4.1/azcopy copy 'evan_chong_9769I.zip' 'https://aisgaice.blob.core.windows.net/aice-associate?sv=2019-02-02&ss=bfqt&srt=co&sp=rwac&se=2020-04-26T15:59:59Z&st=2020-04-18T09:45:14Z&spr=https&sig=zRGXnR9czev%2FTIhhVrEdkQ9kwoAnZsDIx2%2FJycTxCg4%3D'
