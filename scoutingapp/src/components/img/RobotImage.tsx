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

  useEffect(() => {
    const interval = setInterval(() => {
      if (robotNumber) {
        setComponentInside(
          <img
            style={{ width: "50%", height: "50%", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
            src={`./src/components/img/${robotNumber}.png`}
            alt={`Image of robot ${robotNumber} not found.`}
          />
        )
      } else {
        setComponentInside(
          <img
            style={{ width: "50%", height: "50%", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
            src={`./src/components/img/gray.png`}
            alt={'Insert robot number above'}
          />
        )
      }
    }, 500)
    return () => clearInterval(interval);
  })

  return (<>
    {componentInside}
  </>)
}