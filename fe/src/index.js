import React from "react";
import ReactDOM from "react-dom";
// import App from "./app/App";
import "./index.css";
import AppWrp from "./app/AppWrp";
ReactDOM.render(<AppWrp classname={"app"} />, document.getElementById("root"));
// import React from "react";
// import ReactDOM from "react-dom";
// import singleSpaReact from "single-spa-react";
// import AppWrp from "./app/AppWrp";
// import "./index.css";
// const lifecycles = singleSpaReact({
//     React,
//     ReactDOM,
//     rootComponent: AppWrp,
//     // eslint-disable-next-line no-unused-vars
//     errorBoundary(err, info, props) {
//         // Customize the root error boundary for your microfrontend here.
//         return null;
//     },
// });
//
// export const { bootstrap, mount, unmount } = lifecycles;
