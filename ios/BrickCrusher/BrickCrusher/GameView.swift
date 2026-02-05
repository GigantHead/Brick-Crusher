import SwiftUI
import SpriteKit

struct GameView: View {
    @State private var scene: GameScene

    init() {
        let scene = GameScene(size: UIScreen.main.bounds.size)
        scene.scaleMode = .resizeFill
        _scene = State(initialValue: scene)
    }

    var body: some View {
        SpriteView(scene: scene)
            .ignoresSafeArea()
    }
}
