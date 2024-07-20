import React from "react"
import { ComponentSetup } from "../interface"

function RobotImage(props: ComponentSetup, robot_number: number) {
  return (
    <img
      style={{ width: "80%", height: "80%", alignItems: 'center', justifyContent: 'center'}}
      src={`./${robot_number}.png}`}
      alt={`Picture of robot ${robot_number}`}
    />
  )
}