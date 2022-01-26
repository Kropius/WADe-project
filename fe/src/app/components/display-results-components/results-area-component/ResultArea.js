import React, { forwardRef, useEffect, useImperativeHandle, useState } from "react";
import ResultsAreaStyle from "./ResultArea.module.css";
import isEmpty from "lodash/isEmpty";
import RequestMessage from "../message-component/RequestMessage";
import ResponseMessage from "../message-component/ResponseMessage";
import {useAppContext} from "../../../context/AppContext";
import NLPApi from "../../../api/NLPApi";
import PubSub from "pubsub-js";

// eslint-disable-next-line react/display-name
const ResultsArea = forwardRef((props, ref) => {

    const [messages, setMessages] = useState([]);

    const [nlpResult, setNlpResult] = React.useState({});
    // eslint-disable-next-line no-unused-vars
    const {appState} = useAppContext();

    // eslint-disable-next-line no-unused-vars
    const processNLP =
        async(resource, specId) => {
                props?.setIsLoading(true);
            await NLPApi().processNLP(resource, specId)
                .then((fullResponse) =>{console.log(fullResponse);        props?.setIsLoading(false);

                    setNlpResult({message:fullResponse, isRequest: false});})
                .catch((error) => {console.log(error);
                    props?.setIsLoading(false);
                    PubSub.publish("networkError",
                    {title: "Something went wrong with your request",error });});
        };

    // eslint-disable-next-line no-unused-vars
    const mockPost = async() =>{
        await NLPApi().mockPost()
            .then((fullResponse) => console.log(fullResponse))
            .catch((error) => console.log(error));
    };

    useEffect(() => {
        if(!isEmpty(props?.newRequest?.message)){
            processNLP({text_content: props?.newRequest?.message},
                appState?.selectedSpecification?.value);
            console.log(props?.newRequest);
            setMessages([...messages, props?.newRequest]);
        }


    }, [props?.newRequest]);

    useEffect(() => {
        setMessages([...messages, nlpResult]);
    }, [nlpResult]);
    useImperativeHandle(ref, () => {
        return {
            setMessages: setMessages,
        };
    });
    console.log(messages);
    return (
        <div className={ResultsAreaStyle.container}>
            {messages.map(
                (message) =>
                    !isEmpty(message.message) && [
                        message.isRequest ? (
                            <RequestMessage message={message.message} />
                        ) : (
                            <ResponseMessage message={message?.message?.data} />
                        ),
                    ]
            )}
        </div>
    );
});

export default ResultsArea;
