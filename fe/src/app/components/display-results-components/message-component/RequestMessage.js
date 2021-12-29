import React from "react";
import MessageStyle from "./Message.module.css";

const Message = ({message}) => {
    return (
        <div className={`${MessageStyle.bubble} ${MessageStyle.left}`}>{message}</div>

    )
}
export default Message;
