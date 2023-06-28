# ==============================================================================
# 345678901234567890123456789012345678901234567890123456789012345678901234567890
# ==============================================================================
"""
αβ枝刈り(alpha-beta pruning)を伴う，Negamax法

    2021-05-19 IIJIMA, Tadashi
    (Original: Copyright (c) 2013 Zulko The MIT License)

  * 本来は，pip install easyAIで使用可能になるが...
    * 今回はこの先の改良のためにあえてソースコードを取り込んでいる．
    * https://pypi.org/project/easyAI/
  * ソースコード入手元:
    * https://github.com/Zulko/easyAI
"""

# ==============================================================================

inf = float( 'infinity' )

# ==============================================================================
# ===== [関数] αβ枝刈り(alpha-beta pruning)を伴う，Negamax法
# ==============================================================================
def negamax( game_state, depth, orig_depth, scoring, alpha=+inf, beta=-inf ):
    """ αβ枝刈り(alpha-beta pruning)を伴う，Negamax法.

    """
    # ==========================================================================
    #alphaOrig = alpha
    # ==========================================================================
    if ( depth == 0 ) or game_state.is_over():
        score = scoring( game_state )
        if score == 0:
            return( score )
        else:
            return( ( score - 0.01 * depth * abs( score ) / score ) )
    # ==========================================================================
    possible_moves = game_state.possible_moves()
    # --------------------------------------------------------------------------
    state = game_state
    best_move = possible_moves[ 0 ]
    # --------------------------------------------------------------------------
    if depth == orig_depth:
        state.ai_move = possible_moves[ 0 ]
    # --------------------------------------------------------------------------
    bestValue = -inf
    # ==========================================================================
    for move in possible_moves:
        # ----------------------------------------------------------------------
        game_state = state.copy()
        # ----------------------------------------------------------------------
        game_state.make_move( move )
        game_state.switch_player()
        # ----------------------------------------------------------------------
        move_alpha = - negamax( game_state, depth-1, orig_depth, scoring,
                               -beta, -alpha )
        # ----------------------------------------------------------------------
        # bestValue = max( bestValue,  move_alpha )
        if bestValue < move_alpha:
            bestValue = move_alpha
            best_move = move
        # ----------------------------------------------------------------------
        if  alpha < move_alpha:
            alpha = move_alpha
            # best_move = move
            if depth == orig_depth:
                state.ai_move = move
            if ( alpha >= beta ):
                break
        # ----------------------------------------------------------------------
    # ==========================================================================
    return( bestValue )
    # ==========================================================================


# ==============================================================================
# ===== [クラス] Negamax
# ==============================================================================
class Negamax:
    """ Negamaxクラス.
    
    """

    # ==========================================================================
    # ===== [イニシャライザ] 初期化する ======================================== 
    # ==========================================================================
    def __init__( self, depth, scoring=None, win_score=+inf ):
        """ 初期化する.
        """
        # ======================================================================
        self.scoring = scoring        
        self.depth = depth
        self.win_score= win_score
        # ======================================================================

    # ==========================================================================
    # ===== [メソッド] ゲームの現在の状態から与えられる最善手を返す ============
    # ==========================================================================
    def __call__( self, game ):
        """ ゲームの現在の状態から与えられる最善手を返す.
        """
        # ======================================================================
        scoring = self.scoring if self.scoring else (
                       lambda g: g.scoring() ) # horrible hack
                       
        self.alpha = negamax( game, self.depth, self.depth, scoring,
                              -self.win_score, +self.win_score )
        # ======================================================================
        return( game.ai_move )
        # ======================================================================


# ==============================================================================
