import SpeechRecognition, {useSpeechRecognition} from "react-speech-recognition";
import {Button} from "@awsui/components-react";
import {useEffect} from "react";

const Dictaphone = ({handleInputChange, text}) => {
    const {
        transcript,
        listening,
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();
    console.log(handleInputChange);

    useEffect(() => {
        if(handleInputChange){
            handleInputChange(transcript);
        }
    }, [transcript])

    if (!browserSupportsSpeechRecognition) {
        return <span>Browser doesn't support speech recognition.</span>;
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
