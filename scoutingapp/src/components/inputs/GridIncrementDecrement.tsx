import { ComponentSetup } from "../interface"
import React, { useEffect, useState } from "react"

function GridIncrementDecrement(props: ComponentSetup) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    props.setValue({
      ...props.getValue,
      [props.id]: `${count}`,
    })
  }, [count])

  return (
    <div className="mx-3 my-3">
      <label className="block text-[#344054] text-sm mb-2">
        {props.text}
      </label>

      <div className={`grid grid-cols-${props.options?.length} grid-rows-2 gap-3`}>
        {props.options?.map((option: string, idx) => {
          const [raw, label] = option.split("|")
          const n = Number(raw)

          return (
            <button
              key={idx}
              onClick={() => setCount(s => Math.max(0, s - n))}
              className={`h-14 rounded-lg text-lg text-black font-semibold
              bg-[#FDE7E7] hover:opacity-90 transition`}
            >
              - {label}
            </button>
          )
        })}

        {props.options?.map((option: string, idx) => {
          const [raw, label] = option.split("|")
          const n = Number(raw)

          return (
            <button
              key={idx}
              onClick={() => setCount(s => Math.max(0, s + n))}
              className={`h-14 rounded-lg text-lg text-black font-semibold
              bg-[#E2F8E3] hover:opacity-90 transition`}
            >
              + {label}
            </button>
          )
        })}
      </div>

      <div className="mt-4 h-14 rounded-xl bg-amber-300 flex items-center justify-center text-xl font-semibold">
        {count}
      </div>
    </div>
  )
}

export default GridIncrementDecrement
