import React, {useEffect, useState} from "react";
import {Box, ExpandableSection, Flashbar} from "@awsui/components-react";
import PubSub from "pubsub-js";
import style from "./AlertService.module.css";

const AlertService = () => {
    const [state, setState] = useState({alertsCounter :0,
                                                    alerts:[]}
    );
    const handleNetworkErrors = (msg, data) => {
        return setState((prevState) =>{
            const newAlert = buildAlert(data, "error", prevState.alertsCounter);
            return {...prevState,
            alertsCounter: prevState.alertsCounter + 1,
            alerts: [...prevState.alerts, newAlert]};
        } );
    };

    function buildAlert(data, type, index){
        const alertId = `alert-${type}-${index}`;
        return {
            id: alertId,
            header: "Something went wrong with the request",
            type: type,
            content: buildAlertContent(data?.error),
            dismissible: true,
            action: dismissByDefault(alertId),
            onDismiss: () => dismissAlert(alertId)
        };
    }
    function buildAlertContent(error){
        const content = {
            message: error?.data?.message ?? "Unknown message",
            code: error?.status ?? "Unknown status"
        };
        return (<ExpandableSection header={"Error content"}>
            <Box>
                <p>Returned message: {content?.message}</p>
                <p>Failed with HTTP code: {content?.code}</p>
            </Box>
        </ExpandableSection>);
    }
    function dismissAlert(alertId){
        return setState((prevState) =>{
            return {...prevState,
            alerts: prevState.alerts.filter((item)=> item.id !== alertId)};
        } );
    }

    function dismissByDefault(alertId) {
        setTimeout(() => {
            dismissAlert(alertId);
        }, 10000);
    }

    useEffect(()=>
    {
        PubSub.subscribe("networkError", handleNetworkErrors);
        return () => PubSub.unsubscribe("networkError");
    },[]);

    return <Flashbar items={state.alerts} key={`alert ${alert}`} className={style.alertContent}/>;
};

export default AlertService;