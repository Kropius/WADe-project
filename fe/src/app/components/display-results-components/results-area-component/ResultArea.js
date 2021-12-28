import React, {useEffect, useState} from "react";
import ResultsAreaStyle from "./ResultArea.module.css";
import Message from "../message-component/Message";
import isEmpty from "lodash/isEmpty";

const ResultsArea = ({newRequest}) => {
    const [messages, setMessages] = useState([]);
    useEffect(() => {
        setMessages([...messages, newRequest]);
        console.log(newRequest);
    }, [newRequest])
    return (
        <div className={ResultsAreaStyle.container}>
            {messages.map((message) => ([<Message message={message.message}
                                                                           isRequest={message.isRequest}/>,
                    <Message message={"SALUT ACESTA ESTE UN RASPUNS LA REQUEST"}
                             isRequest={!message.isRequest}/>]
            ))}
        </div>);
}
export default ResultsArea;
