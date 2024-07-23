import React, {useEffect, useState} from "react"
import { ComponentSetup } from "../interface"
import QRCode from "react-qr-code";

export const emptyImage = <img
  style={{width: "80%", height: "80%", alignItems: 'center', justifyContent: 'center'}}
  src='../img/gray.png'
  alt={`Picture of robot`}
/>

export function RobotImage(props: ComponentSetup) {
  const [componentInside, setComponentInside] = useState(<></>)
  const robotNumber = props.getValue["TeamNumber"]

  const makeAltText = (robotNumber: string) => {
    if (robotNumber) {
      return `Picture of robot ${robotNumber}`
    } else {
      return 'Insert robot number above'
    }
  }

  useEffect(() => {
    const interval = setInterval(() => {
      setComponentInside(
        <img
          style={{height: "60%", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
          src={`./src/components/img/${robotNumber}.png`}
          alt={makeAltText(robotNumber)}
        />
      )
    }, 500);
    return () => clearInterval(interval);
  })

  return (<>
    {componentInside}
  </>)
}