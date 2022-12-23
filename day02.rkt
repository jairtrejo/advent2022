#lang racket

(require qi)
(require rebellion/streaming/transducer)
(require rebellion/streaming/reducer)
(require syntax/parse/define)

(define (decrypt-my-move move)
  (cond [(equal? move "X") 'rock]
        [(equal? move "Y") 'paper]
        [(equal? move "Z") 'scissors]))

(define (decrypt-result result)
  (cond [(equal? result "X") 'lose]
        [(equal? result "Y") 'draw]
        [(equal? result "Z") 'win]))

(define (decrypt-their-move move)
  (cond [(equal? move "A") 'rock]
        [(equal? move "B") 'paper]
        [(equal? move "C") 'scissors]))

(define (beats move)
  (cond [(equal? move 'rock) 'scissors]
        [(equal? move 'paper) 'rock]
        [(equal? move 'scissors) 'paper]))

(define (score opponent me)
  (+ (cond [(equal? me 'rock) 1]
           [(equal? me 'paper) 2]
           [(equal? me 'scissors) 3])
     (cond [(equal? me (beats opponent)) 0]
           [(equal? me opponent) 3]
           [(equal? (beats me) opponent) 6])))

(define (play opponent result)
  (cond [(equal? result 'lose) (beats opponent)]
        [(equal? result 'draw) opponent]
        [(equal? result 'win) (findf
                                 (lambda (m) (equal? (beats m) opponent))
                                 '(rock paper scissors))]))

(define-flow parse (~> (string-split " ") △))

(define-flow process-part-one
  (~> parse
      (== decrypt-their-move
          decrypt-my-move)
      score))

(define-flow process-part-two
  (~> parse
      (== decrypt-their-move
          decrypt-result)
      (-< 1> play)
      score))

(define part-one
  (into-transduced (mapping process-part-one) #:into into-sum))

(define part-two
  (into-transduced (mapping process-part-two) #:into into-sum))

; Take a file as a command line argument and set it as the default input port.
; Falls back to stdin if no file is provided.
;
; Inspired by python's fileinput module.
(define-syntax-parse-rule (with-fileinput rhs:expr)
  (command-line
    #:program "advent-of-code"
    #:args ([filename '()])
    (parameterize 
      ([current-input-port (if (null? filename) current-input-port (open-input-file filename))])
      rhs)))

(with-fileinput
  (transduce (in-lines) #:into (reducer-zip list part-one part-two)))
