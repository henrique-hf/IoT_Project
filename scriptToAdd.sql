---23-05-2017

ALTER TABLE `tracking`.`p_t`
DROP PRIMARY KEY,
ADD PRIMARY KEY (`packetid`);

ALTER TABLE `tracking`.`p_t`
ADD COLUMN `delivered` INT NULL DEFAULT 0 AFTER `truckid`;