import React, { forwardRef, useEffect, useImperativeHandle, useState } from "react";
import ResultsAreaStyle from "./ResultArea.module.css";
import isEmpty from "lodash/isEmpty";
import RequestMessage from "../message-component/RequestMessage";
import ResponseMessage from "../message-component/ResponseMessage";
import {useAppContext} from "../../../context/AppContext";
import NLPApi from "../../../api/NLPApi";

// eslint-disable-next-line react/display-name
const ResultsArea = forwardRef((props, ref) => {

    const [messages, setMessages] = useState([]);

    const [nlpResult, setNlpResult] = React.useState({});
    const {appState} = useAppContext();

    const processNLP =
        async(resource, specId) => {
                props?.setIsLoading(true);
            await NLPApi().processNLP(resource, specId)
                .then((fullResponse) =>{props?.setIsLoading(false);

                    setNlpResult({message:fullResponse, isRequest: false});})
                .catch(() => {
                    props?.setIsLoading(false);
                   });
        };


    useEffect(() => {
        if(!isEmpty(props?.newRequest?.message)){
            processNLP({text_content: props?.newRequest?.message},
                appState?.selectedSpecification?.value);
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

    return (
        <div className={ResultsAreaStyle.container}>
            {messages.map(
                (message) =>
                    !isEmpty(message.message) && [
                        message.isRequest ? (
                            <RequestMessage message={message.message} />
                        ) : (
                            <ResponseMessage message={message?.message?.data}
                                             selectedApi = {appState?.selectedSpecification}/>
                        ),
                    ]
            )}
        </div>
    );
});

export default ResultsArea;
