import React from "react"
import { ComponentSetup } from "../interface"

export const emptyImage = <img
  style={{width: "80%", height: "80%", alignItems: 'center', justifyContent: 'center'}}
  src='../img/gray.png'
  alt={`Picture of robot`}
/>

export function RobotImage(props: ComponentSetup) {
  const robotNumber = props.getValue["TeamNumber"]

  const makeAltText = (robotNumber: string) => {
    if (robotNumber) {
      return `Picture of robot ${robotNumber}`
    } else {
      return 'Insert robot number above'
    }
  }

  return (
    <img
      style={{ width: "60%", height: "60%", alignItems: 'center', justifyContent: 'center', margin: "auto" }}
      src={`./src/components/img/${robotNumber}.png`}
      alt={makeAltText(robotNumber)}
    />
  )
}