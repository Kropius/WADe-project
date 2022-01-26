import React from "react";
import SpeechRecognition, {useSpeechRecognition} from "react-speech-recognition";
import {Button} from "@awsui/components-react";
import {useEffect} from "react";

const Dictaphone = ({handleInputChange, text}) => {
    const {
        transcript,
        // eslint-disable-next-line no-unused-vars
        listening,
        // eslint-disable-next-line no-unused-vars
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();

    useEffect(() => {
        if(handleInputChange){
            handleInputChange(transcript);
        }
    }, [transcript]);

    if (!browserSupportsSpeechRecognition) {
        return <span>{"Browser doesn't support speech recognition"}.</span>;
    }

    return (
        <div>
            <Button onClick={
                 SpeechRecognition.startListening
            }>{text}</Button>
        </div>
    );
};
export default Dictaphone;
