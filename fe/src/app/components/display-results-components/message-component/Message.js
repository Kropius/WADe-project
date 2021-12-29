import React from "react";
import MessageStyle from "./Message.module.css";

const Message = ({message, isRequest = false, responseBody, path,}) => {
    return (
        <div className={`${MessageStyle.bubble} ${isRequest ? MessageStyle.left : MessageStyle.right}`}>{message}</div>

    )
}
export default Message;
