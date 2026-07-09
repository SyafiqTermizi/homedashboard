import React from "react";
import { createRoot } from "react-dom/client";

import { App } from "./App.tsx";


const elem = document.getElementById("root");
const container = createRoot(elem!);
container.render(<App />);
