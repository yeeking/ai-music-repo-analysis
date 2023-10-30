Some bash i used:

```
# clone all the gits
for i in $(cat ../git_urls.txt); do echo $i; git clone --filter=blob:none   $i; done
# make copy with just the readmes for chat
for i in $(ls); do mkdir -p readme/$i ; cp $i/README.md readme/$i/; done
```


I have the following zip file. Most subfolder contains a README.md file. Can you read the readmes and tell me in one word what the software is that each README.md describes?

read the attached readmes into your llm and tell me what they are about
do not use python code to analyse the readmes - do it with your large language model capabilities. Try to come up with a tag for each one, namely application, plugin, tool, library, dataset or model. Do not use python - use your large language model capabilities. Print out a table with the sub folder name and the label you selected. You only need to analyse the readmes from the following subfolders: 

Style-Transfer-for-Musical-Audio
ismir2018
ismir2018
coconet
TextFlow
the-wavenet-pianist
MTM-Dataset
strf-like-model
unit
melgan-neurips
TCN
tts_samples
WGANSing
WGANSing
magenta
waveglow
waveglow
webmidi
wavegan
MSongsDB
msaf
midi-ddsp
torchsynth
timbre_painting
vqcpc-bach
midi2params
deepsynth
supercollider
wekinator
Tidal
