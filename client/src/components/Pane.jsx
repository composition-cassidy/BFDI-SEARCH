
function Pane({ children }) {
    return (
        <div className="paneBorder">
            <div className="paneContent">
                {children}
            </div>
        </div>
    )
}

export default Pane
