
function ResultCard(props) {    
    // Highlight text method (peter.bartos on StackOverflow)
    const getHighlightedText = (text, highlight) => {
        // Split text on highlight term, include term itself into parts, ignore case
        const parts = text.split(new RegExp(`(${highlight})`, 'gi'));
        return <span>{parts.map(part => part.toLowerCase() === highlight.toLowerCase() ? <span id="highlight">{part}</span> : part)}</span>;
    }

    const titleCase = (str) => {
        return str.replace(
            /\w\S*/g,
            text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
          );
    }

    const redirect = () => {
        //alert("Redirecting to transcript page.")
        // Open transcript page in a new tab
        window.open(props.result.transcript, '_blank');
    }

    const imageUrl = props.result.thumbnail
        ? props.result.thumbnail
        : props.result.image
          ? props.result.image
          : `/thumbnails/placeholder.jpg`;

    return (
        <div className="resultCard" key={props.result._id}>
            <div className="resultText">
                <div className="top">
                    <span className="heading">{props.result.episode_title}</span>
                    <span className="heading">Season {props.result.season}</span>
                    <span className="heading">{titleCase(props.result.character)}</span>
                </div>
                <div className="bottom">
                  <div className="dialogueBox">
                    <p id="dialogue">{getHighlightedText(props.result.dialogue,props.highlight)}</p>
                  </div>
                </div>
            </div>
            <div className="resultImage">
                <img
                  src={imageUrl}
                  alt="Open transcript page"
                  onError={(e) => {
                    if (e.target.dataset.fallback !== "1") {
                      e.target.dataset.fallback = "1";
                      e.target.src = `/thumbnails/placeholder.jpg`;
                    }
                  }}
                  onClick={redirect}
                />
            </div>
        </div>
    );
}

export default ResultCard;