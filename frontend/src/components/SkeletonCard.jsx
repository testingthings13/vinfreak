export default function SkeletonCard(){
  return (
    <div className="card sk">
      <div className="img sk-anim" />
      <div className="body">
        <div className="line sk-anim" style={{width:"70%"}}/>
        <div className="line sk-anim" style={{width:"40%"}}/>
        <div className="line sk-anim" style={{width:"55%"}}/>
      </div>
    </div>
  );
}
