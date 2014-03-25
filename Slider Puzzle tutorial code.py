
import bpy

import time

from random import randint 

bpy.types.Object.has_moved = bpy.props.BoolProperty(default=False)



framesPerMove = 4
numberOfMoves = 250
numberOfSides = 4
name = "Puzzle 2 Piece "


totalPieces = numberOfSides*numberOfSides
totalCounter = 1


def percentagePrint(printName, total):
    global totalCounter
    
    
    percent = (totalCounter/total)*100

    print("     "+printName+" "+str(round(percent))+"% complete")
    
    
    totalCounter+=1
   
   
def cleanScene():
    totalDeleted=1
    
    print("-------------------------------------")
    print("-------------------------------------")    

    print("Detecting and deleting initial objects...")

    bpy.context.scene.layers = [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,]   
    
    if bpy.context.mode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
        
    bpy.ops.object.select_all(action='DESELECT')
    
    for object in bpy.context.scene.objects:
        if name in object.name:
            
            object.select = True
            bpy.ops.object.delete()
            
            print("     Deleted "+str(totalDeleted)+" objects")
            totalDeleted+=1
            
            
    bpy.data.objects['projector'].user_clear()
    bpy.data.images['Texture.png'].user_clear()
    
    print("Deleted "+str(totalDeleted-1)+" objects")
    

def createGrid():
    global totalCounter
    totalCounter = 1
    nameCounter = 1
    
    print("---------------------------------------------")
    print("Creating Grid...")
    
    bpy.context.scene.layers[4] = True
    
    for i in range(0,numberOfSides):
        
        for j in range(0,numberOfSides):
        
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active = bpy.data.objects['OriginalSquare']
            bpy.data.objects['OriginalSquare'].select = True
            bpy.ops.object.duplicate()
            bpy.ops.object.select_all(action='DESELECT')
            
            currentPiece = bpy.context.active_object
            currentPiece.layers[0] = True
            currentPiece.layers[4] = False
            currentPiece.location[0] = i - (numberOfSides/2) + 0.5
            currentPiece.location[1] = j - (numberOfSides/2) + 0.5
            
            currentPiece.name = name+str(nameCounter)
            
            nameCounter+=1
            
            percentagePrint("Grid", totalPieces)
            
    
    bpy.context.scene.layers[4] = False
    
    print("Grid Created")
    
    
def unwrap():
    
    global totalCounter
    totalCounter = 1
    
    print("---------------------------------------------")
    print("Unwrapping...")
    
    texture = bpy.data.images['Texture.png']
    
    bpy.data.objects['projector'].scale = (numberOfSides/2,numberOfSides/2,1)
    
    for i in range(1,totalPieces+1):
        
        currentPiece = bpy.data.objects[name+str(i)]
        
        currentPiece.modifiers.new(name="UVPROJECT", type="UV_PROJECT")
        
        modifier = currentPiece.modifiers[0]
        
        modifier.image = texture
        modifier.projectors[0].object = bpy.data.objects['projector']
        modifier.use_image_override = True
        
        bpy.context.scene.objects.active = currentPiece
        bpy.ops.object.modifier_apply(modifier="UVPROJECT")
           
        percentagePrint("Unwrapping", totalPieces)
           
    print("Unwrapped")


def findEmptyPiece():
    
    print("-------------------------------------------")

    emptyPiece = bpy.data.objects[name+"1"]
    emptyPiece.draw_type = "SOLID"
    emptyPiece.hide_render = True
    
    print("Empty Piece is: "+emptyPiece.name)
    
    return emptyPiece
    

def animatePieces():
    
    global totalCounter
    totalCounter = 1
    
    oldPiece = ""
       
    emptyPiece = findEmptyPiece()
    
    print("---------------------------------------------")
    print("Animating...")
    
    bpy.context.scene.frame_end = (numberOfMoves*framesPerMove)+1
    bpy.context.scene.frame_set((numberOfMoves*framesPerMove)+1)
    
    
    for j in range(0,numberOfMoves):
        priorityPieces = []
        moveablePieces = []
        for i in range(1,totalPieces):
            #answer=" "
            
            currentPiece = bpy.data.objects[name+str(i+1)]
            currentX = round(currentPiece.location[0],2)
            currentY = round(currentPiece.location[1],2)
            emptyX = round(emptyPiece.location[0],2)
            emptyY = round(emptyPiece.location[1],2)
            
            if currentY == emptyY and currentX == emptyX+1 or currentX == emptyX and currentY == emptyY+1 or \
               currentY == emptyY and currentX == emptyX-1 or currentX == emptyX and currentY == emptyY-1:
                #answer=" Match"
                moveablePieces.append(currentPiece)
                
                if len(moveablePieces)==4:
                    break
    
            #print("Comparing: "+currentPiece.name+" "+str(currentY)+" with "+str(emptyY)+" and "+str(currentX)+" with "+str(emptyX)+answer)
            
        
        for piece in moveablePieces:
            if piece.has_moved == False:
                priorityPieces.append(piece)
                
        if len(priorityPieces)>0:
            moveablePieces = priorityPieces
        
            
        numberOfPieces = len(moveablePieces)-1
        
        movingPiece = moveablePieces[randint(0,numberOfPieces)]
        
        while(movingPiece == oldPiece):
            movingPiece = moveablePieces[randint(0,numberOfPieces)]
        oldPiece = movingPiece
        movingPiece.has_moved = True

        
        oldPieceX = movingPiece.location[0]
        oldPieceY = movingPiece.location[1]
        
        movingPiece.keyframe_insert(data_path="location", index=0)
        movingPiece.keyframe_insert(data_path="location", index=1)

        emptyPiece.keyframe_insert(data_path="location", index=0)
        emptyPiece.keyframe_insert(data_path="location", index=1)
        
        bpy.context.scene.frame_set(bpy.context.scene.frame_current-framesPerMove)
        
        movingPiece.location[0] = emptyPiece.location[0]
        movingPiece.location[1] = emptyPiece.location[1]
        emptyPiece.location[0] = oldPieceX
        emptyPiece.location[1] = oldPieceY
        
        movingPiece.keyframe_insert(data_path="location", index=0)
        movingPiece.keyframe_insert(data_path="location", index=1)

        emptyPiece.keyframe_insert(data_path="location", index=0)
        emptyPiece.keyframe_insert(data_path="location", index=1)
        
        percentagePrint("Animation", numberOfMoves)    
            
    print("Animating pieces complete")

    
cleanScene()
 
 
gridStart = time.clock()   
createGrid()
gridTime = str('%0.3f s' % (time.clock()-gridStart))



unwrappingStart = time.clock()
unwrap()
unwrappingTime = str('%0.3f s' % (time.clock()-unwrappingStart))

animatePieces()

print("")
print("Creating pieces took:    "+gridTime)

print("")
print("Unwrapping pieces took:    "+unwrappingTime)


print("Finished")