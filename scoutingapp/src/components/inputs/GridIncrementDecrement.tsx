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
      <label className="block text text-sm mb-2">
        {props.text}
      </label>

      <div className={`grid grid-rows-2 gap-3`} style={{ gridTemplateColumns: `repeat(${props.options?.length}, minmax(0, 1fr))` }}>
        {props.options?.map((option: string, idx) => {
          const [raw, label] = option.split("|")
          const n = Number(raw)

          return (
            <button
              key={idx}
              onClick={() => setCount(s => Math.max(0, s - n))}
              className={`h-14 rounded-lg text-lg text-[var(--text-color)] font-semibold
              bg-[var(--default-pale-red)] hover:opacity-90 transition`}
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
              className={`h-14 rounded-lg text-lg text-[var(--text-color)] font-semibold
              bg-[var(--default-pale-green)] hover:opacity-90 transition`}
            >
              + {label}
            </button>
          )
        })}
      </div>

      <div className="mt-4 h-14 rounded-xl bg-[var(--default-deep-yellow)] flex items-center justify-center text-xl font-semibold text-[var(--text-color)]">
        {count}
      </div>
    </div>
  )
}

export default GridIncrementDecrement
