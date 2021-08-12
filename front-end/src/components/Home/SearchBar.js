const BarStyling = {
  width: "20rem",
  background: "#F2F1F9",
  padding: "0.5rem",
  "margin-top": "1%",
};

const SearchBar = ({ keyword, setKeyword }) => {
  return (
    <div>
      <input
        style={BarStyling}
        key="random1"
        value={keyword}
        placeholder={"Search a pet"}
        // onChange={(e) => setKeyword(e.target.value)
      />
      <button> Search </button>
    </div>
  );
};

export default SearchBar;
