# LevelDB Export

This package allows to export documents from a LevelDB file. For instance it can be used to extract documents from a previously created Firestore export. Note, this package is a fork from [labbots/firestore-export-json](https://github.com/labbots/firestore-export-json). This fork is different in:

1. Makes it an installable package. The original is designed to run as a script.
2. Solves some parsing issues regarding arrays.
