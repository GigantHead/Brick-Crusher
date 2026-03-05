import SpriteKit
import UIKit

final class GameScene: SKScene, SKPhysicsContactDelegate {
    private enum GameState {
        case splash
        case playing
        case gameOver
    }

    private struct PhysicsCategory {
        static let ball: UInt32 = 1 << 0
        static let paddle: UInt32 = 1 << 1
        static let brick: UInt32 = 1 << 2
        static let edge: UInt32 = 1 << 3
    }

    private var gameState: GameState = .splash

    private let paddle = SKSpriteNode(color: .white, size: CGSize(width: 120, height: 20))
    private let ball = SKShapeNode(circleOfRadius: 10)
    private let columns = 8

    private var brickNodes: [SKSpriteNode] = []
    private var lastUpdateTime: TimeInterval = 0
    private var lastBrickTime: TimeInterval = 0

    private let brickHeight: CGFloat = 40
    private let brickSpeed: CGFloat = 120
    private let ballSpeed: CGFloat = 320

    // Score
    private var score = 0
    private let scoreLabel = SKLabelNode(fontNamed: "AvenirNext-Bold")

    private let splashTitle = SKLabelNode(fontNamed: "AvenirNext-Bold")
    private let splashPrompt = SKLabelNode(fontNamed: "AvenirNext-Medium")
    private let gameOverTitle = SKLabelNode(fontNamed: "AvenirNext-Bold")
    private let gameOverPrompt = SKLabelNode(fontNamed: "AvenirNext-Medium")

    private var brickWidth: CGFloat {
        size.width / CGFloat(columns)
    }

    private var brickSpawnInterval: TimeInterval {
        TimeInterval((brickHeight * 2) / brickSpeed)
    }

    // Impact Generator for Haptics
    private let impactGenerator = UIImpactFeedbackGenerator(style: .medium)

    override func didMove(to view: SKView) {
        backgroundColor = .black
        physicsWorld.contactDelegate = self
        physicsBody = SKPhysicsBody(edgeLoopFrom: frame)
        physicsBody?.categoryBitMask = PhysicsCategory.edge

        setupPaddle()
        setupBall()
        setupLabels()
        layoutForCurrentSize()

        impactGenerator.prepare()

        setState(.splash)
    }

    override func didChangeSize(_ oldSize: CGSize) {
        layoutForCurrentSize()
    }

    private func setupPaddle() {
        paddle.zPosition = 1
        paddle.physicsBody = SKPhysicsBody(rectangleOf: paddle.size)
        paddle.physicsBody?.isDynamic = false
        paddle.physicsBody?.categoryBitMask = PhysicsCategory.paddle
        paddle.physicsBody?.collisionBitMask = PhysicsCategory.ball
        addChild(paddle)
    }

    private func setupBall() {
        ball.fillColor = .white
        ball.strokeColor = .clear
        ball.zPosition = 2
        ball.physicsBody = SKPhysicsBody(circleOfRadius: 10)
        ball.physicsBody?.isDynamic = true
        ball.physicsBody?.restitution = 1.0
        ball.physicsBody?.friction = 0
        ball.physicsBody?.linearDamping = 0
        ball.physicsBody?.allowsRotation = false
        ball.physicsBody?.usesPreciseCollisionDetection = true
        ball.physicsBody?.categoryBitMask = PhysicsCategory.ball
        ball.physicsBody?.collisionBitMask = PhysicsCategory.edge | PhysicsCategory.paddle | PhysicsCategory.brick
        ball.physicsBody?.contactTestBitMask = PhysicsCategory.paddle | PhysicsCategory.brick
        addChild(ball)

        // Add trail
        if let trail = SKEmitterNode(fileNamed: "BallTrail") {
            trail.targetNode = self
            ball.addChild(trail)
        } else {
             // Fallback programmatic trail if file not found
             let trail = SKEmitterNode()
             trail.particleTexture = nil // Use square particles (default when nil) instead of missing image
             trail.particleSize = CGSize(width: 4, height: 4)
             trail.particleBirthRate = 20
             trail.particleLifetime = 0.5
             trail.particlePositionRange = CGVector(dx: 5, dy: 5)
             trail.particleColor = .white
             trail.particleAlpha = 0.5
             trail.particleAlphaSpeed = -1.0
             trail.particleScale = 0.8
             trail.particleScaleSpeed = -0.4
             trail.targetNode = self
             ball.addChild(trail)
        }
    }

    private func setupLabels() {
        splashTitle.text = "Brick Crusher"
        splashTitle.fontSize = 44
        splashTitle.fontColor = .cyan

        splashPrompt.text = "Tap to start"
        splashPrompt.fontSize = 20
        splashPrompt.fontColor = .white

        gameOverTitle.text = "Game Over"
        gameOverTitle.fontSize = 44
        gameOverTitle.fontColor = .magenta

        gameOverPrompt.text = "Tap to restart"
        gameOverPrompt.fontSize = 20
        gameOverPrompt.fontColor = .white

        scoreLabel.fontSize = 24
        scoreLabel.fontColor = .white
        scoreLabel.horizontalAlignmentMode = .left
        scoreLabel.text = "Score: 0"

        addChild(splashTitle)
        addChild(splashPrompt)
        addChild(gameOverTitle)
        addChild(gameOverPrompt)
        addChild(scoreLabel)
    }

    private func layoutForCurrentSize() {
        physicsBody = SKPhysicsBody(edgeLoopFrom: frame)
        physicsBody?.categoryBitMask = PhysicsCategory.edge

        let paddleY = max(60, size.height * 0.12)
        paddle.position = CGPoint(x: size.width / 2, y: paddleY)

        ball.position = CGPoint(x: size.width / 2, y: paddleY + 60)

        splashTitle.position = CGPoint(x: size.width / 2, y: size.height * 0.65)
        splashPrompt.position = CGPoint(x: size.width / 2, y: size.height * 0.45)
        gameOverTitle.position = CGPoint(x: size.width / 2, y: size.height * 0.65)
        gameOverPrompt.position = CGPoint(x: size.width / 2, y: size.height * 0.45)

        scoreLabel.position = CGPoint(x: 20, y: size.height - 40)
    }

    private func setState(_ state: GameState) {
        gameState = state

        splashTitle.isHidden = state != .splash
        splashPrompt.isHidden = state != .splash
        gameOverTitle.isHidden = state != .gameOver
        gameOverPrompt.isHidden = state != .gameOver
        scoreLabel.isHidden = state == .splash

        if state == .splash {
            resetGameObjects()
            ball.physicsBody?.velocity = .zero
        }

        if state == .gameOver {
            ball.physicsBody?.velocity = .zero
        }
    }

    private func resetGameObjects() {
        removeAllBricks()
        lastUpdateTime = 0
        lastBrickTime = 0
        score = 0
        updateScore()

        let paddleY = max(60, size.height * 0.12)
        paddle.position = CGPoint(x: size.width / 2, y: paddleY)
        ball.position = CGPoint(x: size.width / 2, y: paddleY + 60)
        ball.physicsBody?.velocity = .zero
    }

    private func updateScore() {
        scoreLabel.text = "Score: \(score)"
    }

    private func startGameIfNeeded() {
        if gameState != .playing {
            setState(.playing)
            ball.physicsBody?.velocity = CGVector(dx: 0, dy: ballSpeed)
        }
    }

    private func endGame() {
        setState(.gameOver)
    }

    private func addBrickRow() {
        let colors: [UIColor] = [.cyan, .magenta, .yellow, .green, .orange, .purple]
        for i in 0..<columns {
            let color = colors.randomElement() ?? .red
            let brick = SKSpriteNode(color: color, size: CGSize(width: brickWidth, height: brickHeight))
            brick.position = CGPoint(x: brickWidth * (CGFloat(i) + 0.5), y: size.height - brickHeight / 2)
            brick.zPosition = 1
            brick.physicsBody = SKPhysicsBody(rectangleOf: brick.size)
            brick.physicsBody?.isDynamic = false
            brick.physicsBody?.categoryBitMask = PhysicsCategory.brick
            brick.physicsBody?.collisionBitMask = PhysicsCategory.ball
            brick.physicsBody?.contactTestBitMask = PhysicsCategory.ball
            addChild(brick)
            brickNodes.append(brick)
        }
    }

    private func removeAllBricks() {
        for brick in brickNodes {
            brick.removeFromParent()
        }
        brickNodes.removeAll()
    }

    private func createExplosion(position: CGPoint, color: UIColor) {
        let emitter = SKEmitterNode()
        emitter.particleTexture = nil // Use square particles if no texture
        emitter.particleSize = CGSize(width: 4, height: 4)
        emitter.particleBirthRate = 100
        emitter.numParticlesToEmit = 20
        emitter.particleLifetime = 0.5
        emitter.particlePositionRange = CGVector(dx: 10, dy: 10)
        emitter.particleSpeed = 100
        emitter.particleSpeedRange = 50
        emitter.emissionAngleRange = .pi * 2
        emitter.particleColor = color
        emitter.particleColorBlendFactor = 1.0
        emitter.particleAlpha = 1.0
        emitter.particleAlphaSpeed = -2.0
        emitter.position = position
        addChild(emitter)

        // Remove emitter after lifetime
        let wait = SKAction.wait(forDuration: 1.0)
        let remove = SKAction.removeFromParent()
        emitter.run(SKAction.sequence([wait, remove]))
    }

    private func shakeCamera(duration: Float, amplitude: CGFloat) {
        let numberOfShakes = duration / 0.04
        var actionsArray: [SKAction] = []
        for _ in 1...Int(numberOfShakes) {
            let moveX = Float(arc4random_uniform(UInt32(amplitude))) - Float(amplitude) / 2
            let moveY = Float(arc4random_uniform(UInt32(amplitude))) - Float(amplitude) / 2
            let shakeAction = SKAction.moveBy(x: CGFloat(moveX), y: CGFloat(moveY), duration: 0.02)
            shakeAction.timingMode = SKActionTimingMode.easeOut
            actionsArray.append(shakeAction)
            actionsArray.append(shakeAction.reversed())
        }

        let actionSeq = SKAction.sequence(actionsArray)
        self.run(actionSeq)
    }

    private func clampPaddle(x: CGFloat) -> CGFloat {
        let halfWidth = paddle.size.width / 2
        return min(max(x, halfWidth), size.width - halfWidth)
    }

    override func update(_ currentTime: TimeInterval) {
        guard gameState == .playing else {
            lastUpdateTime = currentTime
            return
        }

        let delta = lastUpdateTime > 0 ? currentTime - lastUpdateTime : 0
        lastUpdateTime = currentTime

        if currentTime - lastBrickTime >= brickSpawnInterval {
            addBrickRow()
            lastBrickTime = currentTime
        }

        let drop = brickSpeed * CGFloat(delta)
        var remainingBricks: [SKSpriteNode] = []
        for brick in brickNodes {
            brick.position.y -= drop

            if brick.frame.minY <= paddle.frame.maxY {
                endGame()
                break
            }

            if brick.frame.maxY < 0 {
                brick.removeFromParent()
            } else {
                remainingBricks.append(brick)
            }
        }
        brickNodes = remainingBricks

        normalizeBallSpeed()
    }

    private func normalizeBallSpeed() {
        guard gameState == .playing, let body = ball.physicsBody else { return }
        let speed = hypot(body.velocity.dx, body.velocity.dy)
        if speed < 10 {
            body.velocity = CGVector(dx: 0, dy: ballSpeed)
            return
        }
        let scale = ballSpeed / speed
        body.velocity = CGVector(dx: body.velocity.dx * scale, dy: body.velocity.dy * scale)
    }

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = touches.first else { return }
        let location = touch.location(in: self)

        switch gameState {
        case .splash:
            startGameIfNeeded()
        case .gameOver:
            setState(.splash)
        case .playing:
            movePaddle(to: location.x)
        }
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard gameState == .playing, let touch = touches.first else { return }
        let location = touch.location(in: self)
        movePaddle(to: location.x)
    }

    private func movePaddle(to x: CGFloat) {
        paddle.position.x = clampPaddle(x: x)
    }

    func didBegin(_ contact: SKPhysicsContact) {
        guard gameState == .playing else { return }

        let bodies = [contact.bodyA, contact.bodyB]
        guard let ballBody = bodies.first(where: { $0.categoryBitMask == PhysicsCategory.ball }) else { return }
        guard let otherBody = bodies.first(where: { $0 !== ballBody }) else { return }

        if otherBody.categoryBitMask == PhysicsCategory.paddle {
            applyPaddleBounce()
            impactGenerator.impactOccurred()
            shakeCamera(duration: 0.1, amplitude: 5)
            return
        }

        if otherBody.categoryBitMask == PhysicsCategory.brick, let brickNode = otherBody.node as? SKSpriteNode {
            // Particles
            createExplosion(position: brickNode.position, color: brickNode.color)

            brickNode.removeFromParent()
            if let index = brickNodes.firstIndex(of: brickNode) {
                brickNodes.remove(at: index)
            }
            applyBrickBounce(against: brickNode)

            // Haptics & Shake
            impactGenerator.impactOccurred()
            shakeCamera(duration: 0.15, amplitude: 8)

            // Score
            score += 10
            updateScore()
        }
    }

    private func applyPaddleBounce() {
        guard let body = ball.physicsBody else { return }
        let offset = (ball.position.x - paddle.position.x) / (paddle.size.width / 2)
        let clamped = max(-1, min(1, offset))
        let angle = clamped * (.pi / 4)
        let dx = ballSpeed * sin(angle)
        let dy = ballSpeed * cos(angle)
        body.velocity = CGVector(dx: dx, dy: abs(dy))
    }

    private func applyBrickBounce(against brick: SKSpriteNode) {
        guard let body = ball.physicsBody else { return }
        let dx = ball.position.x - brick.position.x
        let dy = ball.position.y - brick.position.y

        var newVelocity = body.velocity
        if abs(dx) > abs(dy) {
            newVelocity.dx *= -1
        } else {
            newVelocity.dy *= -1
        }
        body.velocity = newVelocity
    }
}
