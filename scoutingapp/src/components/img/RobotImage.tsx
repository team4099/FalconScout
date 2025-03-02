import React, {useEffect, useState} from "react"
import { ComponentSetup } from "../interface"

export const emptyImage = <img
  style={{width: "80%", height: "80%", alignItems: 'center', justifyContent: 'center'}}
  src='../gray.png'
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
            style={{ height: "300px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
            src={`../${robotNumber}.jpeg`}
            alt={`Image of robot ${robotNumber} not found.`}
          />
        )
      } else {
        setComponentInside(
          <img
            style={{ height: "300px", alignItems: 'center', justifyContent: 'center', margin: "auto"}}
            src={`../gray.png`}
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