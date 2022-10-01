function GenericTextInput() {

  return (
    <div className="mx-3">
      <label className="block text-[#344054] text-sm mb-2">
        Username
      </label>
      <input className="shadow appearance-none border border-color-[#D0D5DD] rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username"></input>
    </div>
  )
}

export default GenericTextInput
